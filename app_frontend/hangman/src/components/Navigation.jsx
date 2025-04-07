// Komponenta navigačního panelu pro hru Šibenice
export default function Navigation() {
    // Renderování navigačního panelu s názvem hry a tlačítkem zpět
    return (
        // Modrý navigační panel
        <nav className="bg-blue-500 p-4 text-white">
            <div className="max-w-4xl mx-auto flex justify-between items-center">
                <h3 className="text-xl font-semibold">Hangman Game</h3>
                <div>
                    <a href="/" className="text-right text-white hover:text-blue-900 font-semibold">Zpět</a>
                </div>
            </div>
        </nav>
    );
} 
