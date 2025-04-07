// Import React hooks pro správu stavu a životního cyklu komponenty
import { useState, useEffect } from 'react';
// Import komponenty pro navigační panel
import Navigation from './Navigation';
// Import komponenty pro virtuální klávesnici
import Keyboard from './Keyboard';

// Hlavní komponenta implementující logiku hry Šibenice
export default function HangmanGame() {
    // Definice stavových proměnných:
    // - word: aktuální hádané slovo
    // - guessedLetters: množina již hádaných písmen
    // - remainingGuesses: počet zbývajících pokusů
    // - loading: indikátor načítání dat
    const [word, setWord] = useState('');
    const [guessedLetters, setGuessedLetters] = useState(new Set());
    const [remainingGuesses, setRemainingGuesses] = useState(6);
    const [loading, setLoading] = useState(true);

    // Asynchronní funkce pro získání nového slova z API
    const fetchWord = async () => {
        try {
            const response = await fetch('/hangman/api/hangman/word/');
            const data = await response.json();
            setWord(data.word);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching word:', error);
            setWord('HANGMAN'); // fallback word
            setLoading(false);
        }
    };

    // Načtení slova při prvním renderování komponenty
    useEffect(() => {
        fetchWord();
    }, []);

    // Funkce pro zpracování pokusu o uhádnutí písmene
    const guessLetter = (letter) => {
        if (remainingGuesses <= 0) return;
        
        const newGuessedLetters = new Set(guessedLetters);
        newGuessedLetters.add(letter);
        setGuessedLetters(newGuessedLetters);
        
        if (!word.includes(letter)) {
            setRemainingGuesses(remainingGuesses - 1);
        }
    };

    // Vytvoření zobrazovaného slova s podtržítky místo neuhádnutých písmen
    const displayWord = word
        .split('')
        .map(letter => guessedLetters.has(letter) ? letter : '_')
        .join(' ');
        
    // Kontrola stavu hry:
    // - hasWon: true pokud jsou všechna písmena uhádnuta
    // - hasLost: true pokud došly pokusy
    const hasWon = !displayWord.includes('_');
    const hasLost = remainingGuesses <= 0;

    // Renderování herního rozhraní
    return (
        <div>
            {/* Navigační panel */}
            <Navigation />
            {/* Hlavní herní oblast */}
            <div className="max-w-2xl mx-auto p-4">
                {/* Zobrazení hádaného slova a zbývajících pokusů */}
                <div className="mb-8">
                    <p className="text-2xl font-mono mb-4">{displayWord}</p>
                    <p className="text-lg">Remaining guesses: {remainingGuesses}</p>
                </div>
                
                {/* Virtuální klávesnice - zobrazena pouze během aktivní hry */}
                {!hasWon && !hasLost && (
                    <Keyboard 
                        guessedLetters={guessedLetters}
                        onGuess={guessLetter}
                    />
                )}
                
                {/* Panel s výsledkem hry a tlačítkem pro restart */}
                {(hasWon || hasLost) && (
                    <div className="text-center">
                        <p className="text-xl mb-4">
                            {hasWon ? 'Congratulations! You won!' : 'Game Over!'}
                        </p>
                        <button
                            onClick={() => {
                                setWord('HANGMAN');
                                setGuessedLetters(new Set());
                                setRemainingGuesses(6);
                            }}
                            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                        >
                            Play Again
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
} 
