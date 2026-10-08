import { useState } from 'react'




function App() {
  const [shloka, setShloka] = useState('');

  // Store the URL of the generated chant.
  const [audioUrl, setAudioUrl] = useState(null);

  //loading variables 
  const [isLoading, setIsLoading] = useState(false);

 

  async function handleGenerate() {
    setIsLoading(true);
    // Convert the textarea into an array of nonempty lines.
    const lines = shloka
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

  // Send the Sanskrit lines to FastAPI.
  try {
  const response = await fetch("http://127.0.0.1:8000/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: lines,
    }),
  });

   if (!response.ok) {
      throw new Error(`Generation failed: ${response.status}`);
    }


  // Convert the JSON response into a JavaScript object.
  const data = await response.json();

  console.log("API response:", data);

  //Convert the relative audio URL into a full backend URL.
  const fullAudioUrl =`http://127.0.0.1:8000${data.audio_url}`;

  //Save it in React state so the interface updates.
  setAudioUrl(fullAudioUrl);
} catch (error){
  console.error("Chant generation error:",error);
} finally {
  setIsLoading(false);
}
}




  return (
    <main>
      <h1> Peaceful Shlokas </h1>
      <p> Generate beautiful Sanskrit chants using AI </p>

      <label htmlFor="shloka"> Enter your Sanskrit shloka </label>
      <textarea
        id = "shloka"
        value = {shloka}
        onChange = {(event) => setShloka(event.target.value)}
        placeholder = "कराग्रे वसते लक्ष्मीः करमध्ये सरस्वती। करमूले तु गोविन्दः प्रभाते करदर्शनम्॥"
        rows = {5}
      />

      <p> Characters entered: {shloka.length}</p>

      <button
      type="button"
      onClick={handleGenerate}
      disabled={!shloka.trim()|| isLoading}
      >
      {isLoading ? "Generating..." : "Generate Chant"}
      </button>

      {audioUrl && (
        <section>
          <h2> Your Generated Chant </h2>

          <audio controls src={audioUrl}>
            Your browser does not support the audio element.
          </audio>
        </section>
        
      
      )}



    </main>
  );
}

export default App
