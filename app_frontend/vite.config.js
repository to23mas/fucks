// Import funkce pro definici konfigurace Vite
import { defineConfig } from 'vite';
// Import React pluginu pro Vite
import react from '@vitejs/plugin-react';
// Import modulu pro práci s cestami
import path from 'path';

// Export konfigurace Vite
export default defineConfig({
  // Seznam pluginů - v tomto případě pouze React plugin
  plugins: [react()],
  // Kořenový adresář projektu
  root: 'hangman',
  // Základní cesta pro statické soubory
  base: '/static/hangman/',
  // Konfigurace build procesu
  build: {
    // Výstupní adresář pro sestavené soubory
    outDir: path.resolve(__dirname, '../public/static/hangman'),
    // Adresář pro statické assety (obrázky, fonty, atd.)
    assetsDir: 'assets',
    // Generování manifest souboru pro lepší cachování
    manifest: true,
  },
}); 

