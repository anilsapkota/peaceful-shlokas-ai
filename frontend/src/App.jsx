import { useState } from 'react'




function App() {
  const [shloka, setShloka] = useState('');

  function handleGenerate() {
    console.log("Shloka submitted:",shloka); 
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
      disabled={!shloka.trim()}
      >
      Generate Chant
      </button>



    </main>
  );
}

export default App
