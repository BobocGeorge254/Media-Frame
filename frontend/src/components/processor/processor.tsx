import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Oval } from 'react-loader-spinner';
import './processor.css';

interface ProcessorProps {
  token: string;
}

const Processor: React.FC<ProcessorProps> = ({ token }) => {
  const [file, setFile] = useState<File | null>(null);
  const [fileUrl, setFileUrl] = useState<string | null>(null); // URL for submitted file playback
  const [outputUrl, setOutputUrl] = useState<string | null>(null); // URL for result video/audio playback
  const [output, setOutput] = useState<string>(''); // Text output (for transcription)
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const [action, setAction] = useState<
    'transcribe' | 'shift' | 'noisecancel' | 'bassboost' | 'speechidentifier' | 'speedup' | 'video-transcribe'
  >('transcribe'); // Action selector
  const [language, setLanguage] = useState<string>('en'); // Default language for transcription

  // Handle file input change
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files ? e.target.files[0] : null;

    if (selectedFile) {
      const validTypes = ['audio/mp3', 'video/mp4'];
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setFileUrl(URL.createObjectURL(selectedFile));
        setError('');
      } else {
        setFile(null);
        setFileUrl(null);
        setError('Please select a valid MP3 or MP4 file.');
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
      | 'video-transcribe'
    );
    setOutput('');
    setOutputUrl(null);
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
    setOutputUrl(null);

    const formData = new FormData();
    formData.append('file', file);

    if (action === 'transcribe' || action === 'video-transcribe') {
      formData.append('language', language); // Append language only for transcription and video transcription
    }

    const endpointMap: Record<string, string> = {
      transcribe: 'http://127.0.0.1:8000/api/processor/transcribe/',
      shift: 'http://127.0.0.1:8000/api/processor/shift/',
      noisecancel: 'http://127.0.0.1:8000/api/processor/noisecancel/',
      bassboost: 'http://127.0.0.1:8000/api/processor/bassboost/',
      speechidentifier: 'http://127.0.0.1:8000/api/processor/speechidentifier/',
      speedup: 'http://127.0.0.1:8000/api/processor/speedup/',
      'video-transcribe': 'http://127.0.0.1:8000/api/processor/video-transcribe/', // New endpoint
    };

    const endpoint = endpointMap[action];

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (action === 'transcribe') {
        const result = await response.json();
        if (response.ok) {
          setOutput(result.transcript || '');
        } else {
          setError(result.error || 'An error occurred during processing.');
        }
      } else if (action === 'video-transcribe') {
        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          setOutputUrl(url); // Display transcribed video
        } else {
          const result = await response.json();
          setError(result.error || 'An error occurred during processing.');
        }
      } else {
        // Other actions
        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          setOutputUrl(url);
        } else {
          const result = await response.json();
          setError(result.error || 'An error occurred during processing.');
        }
      }
    } catch (err) {
      setError('An error occurred while processing the file.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="Processor">
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
            <option value="video-transcribe">Video Transcription</option>
          </select>
        </div>

        {/* Language selector is shown only for 'transcribe' */}
        {action === 'transcribe' && (
          <div className="form-group">
            <label htmlFor="language-select">Select Language:</label>
            <select
              id="language-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="de">German</option>
              <option value="fr">French</option>
              <option value="ro">Romanian</option>
            </select>
          </div>
        )}

        <div className="form-group">
          <input type="file" accept="audio/mp3,video/mp4" onChange={handleFileChange} />
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>

      {fileUrl && (
        <div className="media-player">
          <h2>Uploaded File:</h2>
          {file?.type.startsWith('audio/') ? (
            <audio controls src={fileUrl}></audio>
          ) : (
            <video controls width="100%" src={fileUrl}></video>
          )}
        </div>
      )}

      {loading && (
        <div className="loading-spinner">
          <Oval height={50} width={50} color="#4fa94d" visible={true} ariaLabel="oval-loading" />
          <p>Processing your file...</p>
        </div>
      )}

      {error && <p className="error-text">{error}</p>}

      {output && action === 'transcribe' && (
        <div className="output-box">
          <h2>Result:</h2>
          <pre>{output}</pre>
        </div>
      )}

      {outputUrl && (
        <div className="media-player">
          <h2>Processed File:</h2>
          {action === 'video-transcribe' ? (
            <video controls width="100%" src={outputUrl}></video>
          ) : (
            <audio controls src={outputUrl}></audio>
          )}
          <a
            href={outputUrl}
            download={`${action === 'video-transcribe' ? 'transcribed_video.mp4' : 'processed_audio.mp3'}`}
            className="download-link"
          >
            Download Processed File
          </a>
        </div>
      )}
    </div>
  );
};

export default Processor;
