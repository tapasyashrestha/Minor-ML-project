# Design System: SMS Spam Detector (Techy Murrey & Alabaster Theme)

## 1. Visual Theme & Atmosphere
A clean, high-contrast, technical interface with a balanced cockpit layout and crisp grid alignment. The theme pairs **Alabaster** (a warm, organic off-white) with **Murrey** (a traditional deep red-purple) to create a premium, editorial-meets-terminal visual identity. 
* **Density:** 7 (Balanced & data-rich)
* **Variance:** 6 (Technical grids, clean alignments, subtle asymmetry)
* **Atmosphere:** A modern, minimal laboratory aesthetic — clinical, precise, and visually commanding.

## 2. Color Palette & Roles
* **Alabaster Canvas** (`#F5F3EC`) — Main background canvas. Off-white with warm, stone-like undertones.
* **Pure Alabaster Surface** (`#FAF9F6`) — Card backgrounds, containers, and main content panels.
* **Deep Murrey Canvas** (`#2D0018`) — Sidebar background, providing a distinct split-screen interface.
* **Bright Murrey Accent** (`#8B004B`) — Primary brand highlight, buttons, progress indicators, and active/focus states.
* **Charcoal Ink** (`#241C1E`) — Main text color, preventing the harshness of pure black while retaining high readability.
* **Muted Rose Steel** (`#756569`) — Secondary/muted text, borders, and description items.
* **Whisper Border** (`rgba(139, 0, 75, 0.15)`) — Fine grid lines and container borders.

## 3. Typography Rules
* **Display / Headings:** `Space Grotesk` — A geometric sans-serif with subtle quirky details, set with tight letter-spacing (`tracking-tight`).
* **Body Text:** `Space Grotesk` — Readable, well-spaced, and clean.
* **Code / Metrics / Monospace:** `Share Tech Mono` — A stylized technical monospace font used for numerical metrics, token arrays, and technical tags.

## 4. Component Stylings
* **Buttons:** Flat rectangles with a crisp `1px` border, featuring a direct `-1px` vertical translation on press. No neon outer glows. Bright Murrey background for primary actions, thin borders with hover text changes for secondary presets.
* **Cards (UI Panels):** Crisp `8px` rounded corners, bordered with fine `1px solid rgba(139, 0, 75, 0.15)`, and a subtle techy header line. Shadows are eliminated in favor of clean border definitions.
* **Metrics:** Highlighted with top borders in Murrey and values rendered in `Share Tech Mono`.
* **Result Alert Boxes:**
  * **Spam Alert:** Light coral/rose background (`#FDF2F4`) with a solid Murrey left-border (`#8B004B`) and deep wine text.
  * **Ham Alert:** Soft light green/cream background (`#F2F7F2`) with a solid green-gray left-border (`#3F6E4C`) and dark sage text.

## 5. Layout & Grid
* Grid-first layout using side-by-side modules for inputs and outputs.
* Background pattern features a subtle digital dot grid in `rgba(139, 0, 75, 0.05)` spaced at `16px`.
* Sidebar behaves as a high-density control center with sharp contrast.

## 6. Anti-Patterns (Banned AI Clichés)
* No generic `Inter` or standard browser system fonts.
* No gradient text on headings.
* No soft, heavy card shadows or neon button glows.
* No emojis in labels/buttons (we use functional icons and text).
* No pure black `#000000`.
