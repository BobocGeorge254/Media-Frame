import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Oval } from 'react-loader-spinner';
import './App.css';

interface TranscriptionResponse {
  transcript?: string;
  error?: string;
}

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [output, setOutput] = useState<string>(''); // For transcription or other outputs
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const [action, setAction] = useState<
    'transcribe' | 'shift' | 'noisecancel' | 'bassboost' | 'speechidentifier' | 'speedup'
  >('transcribe'); // Action selector
  const [nSteps, setNSteps] = useState<number>(2); // Default pitch shift semitones
  const [speedFactor, setSpeedFactor] = useState<number>(1.5); // Default speed-up factor

  // Handle file input change
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files ? e.target.files[0] : null;

    if (selectedFile) {
      // Check if the file is an MP3
      if (selectedFile.type === 'audio/mp3' || selectedFile.name.endsWith('.mp3')) {
        setFile(selectedFile);
        setError('');
      } else {
        setFile(null);
        setError('Please select a valid MP3 file');
      }
    }
  };

  // Handle action change
  const handleActionChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setAction(
      e.target.value as
      | 'transcribe'
      | 'shift'
      | 'noisecancel'
      | 'bassboost'
      | 'speechidentifier'
      | 'speedup'
    );
    setOutput('');
    setError('');
  };

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file before submitting.');
      return;
    }

    setLoading(true);
    setError('');
    setOutput('');

    const formData = new FormData();
    formData.append('file', file);

    if (action === 'shift') {
      formData.append('n_steps', nSteps.toString());
    }

    if (action === 'speedup') {
      formData.append('speed_factor', speedFactor.toString());
    }

    const endpointMap: Record<string, string> = {
      transcribe: 'http://127.0.0.1:8000/api/transcribe/',
      shift: 'http://127.0.0.1:8000/api/shift/',
      noisecancel: 'http://127.0.0.1:8000/api/noisecancel/',
      bassboost: 'http://127.0.0.1:8000/api/bassboost/',
      speechidentifier: 'http://127.0.0.1:8000/api/speechidentifier/',
      speedup: 'http://127.0.0.1:8000/api/speedup/',
    };

    const endpoint = endpointMap[action];

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });

      if (action === 'transcribe' || action === 'speechidentifier') {
        const result: TranscriptionResponse = await response.json();

        if (response.ok) {
          setOutput(result.transcript || '');
        } else {
          setError(result.error || 'An error occurred during processing');
        }
      } else {
        // For noisecancel, bassboost, shift, and speedup
        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          setOutput(url);
        } else {
          const result = await response.json();
          setError(result.error || 'An error occurred during processing');
        }
      }
    } catch (err) {
      setError('An error occurred while processing the file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Audio File Processing</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="action-select">Select Action:</label>
          <select id="action-select" value={action} onChange={handleActionChange}>
            <option value="transcribe">Transcription</option>
            <option value="shift">Pitch Shifting</option>
            <option value="noisecancel">Noise Cancellation</option>
            <option value="bassboost">Bass Boost</option>
            <option value="speechidentifier">Speech Identification</option>
            <option value="speedup">Speed Up</option>
          </select>
        </div>

        {action === 'shift' && (
          <div className="form-group">
            <label htmlFor="pitch-shift">Pitch Shift (Semitones):</label>
            <input
              id="pitch-shift"
              type="number"
              value={nSteps}
              onChange={(e) => setNSteps(Number(e.target.value))}
              min="-12"
              max="12"
            />
          </div>
        )}

        {action === 'speedup' && (
          <div className="form-group">
            <label htmlFor="speed-factor">Speed Factor:</label>
            <input
              id="speed-factor"
              type="number"
              step="0.1"
              value={speedFactor}
              onChange={(e) => setSpeedFactor(Number(e.target.value))}
              min="0.5"
              max="3.0"
            />
          </div>
        )}

        <div className="form-group">
          <input type="file" accept="audio/mp3" onChange={handleFileChange} />
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>

      {loading && (
        <div className="loading-spinner">
          <Oval
            height={50}
            width={50}
            color="#4fa94d"
            visible={true}
            ariaLabel="oval-loading"
            secondaryColor="#4fa94d"
            strokeWidth={2}
            strokeWidthSecondary={2}
          />
          <p>Processing your file...</p>
        </div>
      )}

      {error && <p className="error-text">{error}</p>}

      {output && action === 'transcribe' && (
        <div className="output-box">
          <h2>Transcription:</h2>
          <pre>{output}</pre>
        </div>
      )}

      {output && action === 'speechidentifier' && (
        <div className="output-box">
          <h2>Speech Identification:</h2>
          <pre>{output}</pre>
        </div>
      )}

      {output && (action === 'shift' || action === 'noisecancel' || action === 'bassboost' || action === 'speedup') && (
        <div className="output-box">
          <h2>Processed Audio:</h2>
          <a href={output} download={`${action}_audio.mp3`} className="download-link">
            Download Processed Audio
          </a>
        </div>
      )}
    </div>
  );
};

export default App;
