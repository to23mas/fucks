// Props:
// - guessedLetters: Set již použitých písmen
// - onGuess: callback funkce volaná při kliknutí na písmeno
export default function Keyboard({ guessedLetters, onGuess }) {
    // Vytvoření pole všech písmen abecedy
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    
    // Renderování mřížky tlačítek s písmeny
    return (
        // Grid layout s 7 sloupci a mezerami mezi tlačítky
        <div className="grid grid-cols-7 gap-2">
            {/* Mapování přes abecedu a vytvoření tlačítka pro každé písmeno */}
            {alphabet.map(letter => (
                // Tlačítko s písmenem:
                // - deaktivované pokud už bylo použito
                // - šedé pokud použito, modré pokud dostupné
                <button
                    key={letter}
                    onClick={() => onGuess(letter)}
                    disabled={guessedLetters.has(letter)}
                    className={`p-2 text-center rounded ${
                        guessedLetters.has(letter)
                            ? 'bg-gray-300'
                            : 'bg-blue-500 text-white hover:bg-blue-600'
                    }`}
                >
                    {letter}
                </button>
            ))}
        </div>
    );
} 
