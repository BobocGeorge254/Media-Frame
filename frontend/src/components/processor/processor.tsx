import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Oval } from 'react-loader-spinner';
import "./processor.css";

interface TranscriptionResponse {
  transcript?: string;
  error?: string;
}

interface SpeechIdentifierResponse {
  speech_info?: {
    transcription: string;
    speaker_segments: Array<{
      start_time: number;
      end_time: number;
      speaker: string;
      text: string;
    }>;
  };
  error?: string;
}

interface ProcessorProps {
  token: string;
}

const Processor: React.FC<ProcessorProps> = ({ token }) => {
  const [file, setFile] = useState<File | null>(null);
  const [fileUrl, setFileUrl] = useState<string | null>(null); // URL for submitted file playback
  const [output, setOutput] = useState<string>(''); // For transcription or other outputs
  const [outputUrl, setOutputUrl] = useState<string | null>(null); // URL for result audio playback
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const [action, setAction] = useState<
    'transcribe' | 'shift' | 'noisecancel' | 'bassboost' | 'speechidentifier' | 'speedup'
  >('transcribe'); // Action selector
  const [nSteps, setNSteps] = useState<number>(2); // Default pitch shift semitones
  const [speedFactor, setSpeedFactor] = useState<number>(1.5); // Default speed-up factor
  const [language, setLanguage] = useState<string>('en'); // Default language for transcription

  // Handle file input change
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files ? e.target.files[0] : null;

    if (selectedFile) {
      if (selectedFile.type === 'audio/mp3' || selectedFile.name.endsWith('.mp3')) {
        setFile(selectedFile);
        setFileUrl(URL.createObjectURL(selectedFile)); // Generate URL for playback
        setError('');
      } else {
        setFile(null);
        setFileUrl(null);
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

    if (action === 'shift') {
      formData.append('n_steps', nSteps.toString());
    }

    if (action === 'speedup') {
      formData.append('speed_factor', speedFactor.toString());
    }

    if (action === 'transcribe') {
      formData.append('language', language); // Add selected language to the form data
    }

    const endpointMap: Record<string, string> = {
      transcribe: 'http://127.0.0.1:8000/api/processor/transcribe/',
      shift: 'http://127.0.0.1:8000/api/processor/shift/',
      noisecancel: 'http://127.0.0.1:8000/api/processor/noisecancel/',
      bassboost: 'http://127.0.0.1:8000/api/processor/bassboost/',
      speechidentifier: 'http://127.0.0.1:8000/api/processor/speechidentifier/',
      speedup: 'http://127.0.0.1:8000/api/processor/speedup/',
    };

    const endpoint = endpointMap[action];

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (action === 'transcribe') {
        const result: TranscriptionResponse = await response.json();

        if (response.ok) {
          setOutput(result.transcript || '');
        } else {
          setError(result.error || 'An error occurred during processing');
        }
      } else if (action === 'speechidentifier') {
        const result: SpeechIdentifierResponse = await response.json();

        if (response.ok && result.speech_info) {
          setOutput(JSON.stringify(result.speech_info)); // Store the `speech_info` object for rendering
        } else {
          setError(result.error || 'An error occurred during processing');
        }
      } else {
        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          setOutputUrl(url); // Set URL for playback
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
          </select>
        </div>

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
              {/* Add more languages as required */}
            </select>
          </div>
        )}

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

      {fileUrl && (
        <div className="audio-player">
          <h2>Uploaded File:</h2>
          <audio controls src={fileUrl}></audio>
        </div>
      )}

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
          <h2>Result:</h2>
          <pre>{output}</pre>
        </div>
      )}

      {output && action === 'speechidentifier' && (
        <div className="output-box">
          <h2>Speech Identification Results:</h2>
          <div className="segments-container">
            {(() => {
              try {
                const result = typeof output === 'string' ? JSON.parse(output) : output;

                if (
                  result &&
                  Array.isArray(result.speaker_segments) &&
                  result.speaker_segments.length > 0
                ) {
                  return (
                    <>
                      <div className="transcription-container">
                        <h3>Full Transcription:</h3>
                        <p>{result.transcription}</p>
                      </div>
                      {result.speaker_segments.map((segment: any, index: number) => (
                        <div key={index} className="segment-card">
                          <p><strong>Speaker:</strong> {segment.speaker}</p>
                          <p><strong>Text:</strong> {segment.text}</p>
                          <p>
                            <strong>Start Time:</strong> {segment.start_time.toFixed(2)}s |
                            <strong> End Time:</strong> {segment.end_time.toFixed(2)}s
                          </p>
                        </div>
                      ))}
                    </>
                  );
                } else {
                  return <p>No speaker segments found in the response.</p>;
                }
              } catch (err) {
                console.error("Error parsing speechidentifier response:", err);
                return <p>Error parsing response data.</p>;
              }
            })()}
          </div>
          <button className="download-link" onClick={() => {
            const blob = new Blob([output], { type: 'text/plain' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `speechidentifier_response.txt`;
            link.click();
            URL.revokeObjectURL(link.href);
          }}>
            Download as TXT
          </button>
        </div>
      )}

      {outputUrl && (
        <div className="audio-player">
          <h2>Processed Audio:</h2>
          <audio controls src={outputUrl}></audio>
          <a href={outputUrl} download={`${action}_audio.mp3`} className="download-link">
            Download Processed Audio
          </a>
        </div>
      )}
    </div>
  );
};

export default Processor;
