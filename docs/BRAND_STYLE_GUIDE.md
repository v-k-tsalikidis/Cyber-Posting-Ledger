# AEGIS-LEDGER Brand Style Guide & Design System

*AEGIS Vacancy Intelligence Ledger — Academic & Recruiter-Grounded Cybersecurity Career Intelligence*

---

## 1. Brand Identity & Purpose

**AEGIS-LEDGER** is a local-first tool for assessing cybersecurity vacancies against a structured record of your own experience, using **CyBOK v1.1** and the **NIST NICE Framework** as the vocabulary for the comparison.

The visual language rejects modern AI tropes (bright neon glows, dark glossy cards, decorative emojis) in favor of a **Premium Minimalist** gallery dashboard aesthetic characterized by precision typography, warm paper tones, thin 1px structural hairlines, and desaturated status pills.

---

## 2. Brand Color Palette

```
+-----------------------+-----------------------+-----------------------+
|  Canvas Background    |  Card Surface         |  Hairline Border      |
|  #FAF9F6              |  #FFFFFF              |  #E2E8F0              |
+-----------------------+-----------------------+-----------------------+
|  Primary Ink          |  Muted Ink            |  Brand Accent Teal    |
|  #1E293B              |  #64748B              |  #0F5257              |
+-----------------------+-----------------------+-----------------------+
```

### Desaturated Status Pills

- **Eligible / High Alignment:**
  - Background: `#E6F4F1`
  - Border: `#B8E2DA`
  - Text: `#0F5257`
- **Conditional / Warning:**
  - Background: `#FDF4E7`
  - Border: `#F6DEBD`
  - Text: `#8C531B`
- **Disqualified / High Risk:**
  - Background: `#FDF0F0`
  - Border: `#F9D0D0`
  - Text: `#992B2B`

---

## 3. Typography System

| Element | Font Family | Size | Weight | Line Height / Tracking |
| :--- | :--- | :--- | :--- | :--- |
| **Brand Headers / H1** | `Inter`, sans-serif | `1.25rem` (20px) | `700` | `-0.02em` letter spacing |
| **Section Titles / H2-H3** | `Inter`, sans-serif | `1.05rem` (168x) | `600` | `-0.01em` letter spacing |
| **Body Text** | `Inter`, sans-serif | `0.875rem` (14px) | `400` | `1.5` line height |
| **Data / Numeric Scores** | `JetBrains Mono`, monospace | `1.15rem` (18px) | `600` | Monospaced numeric alignment |

---

## 4. Logo & Iconography Specifications

### Vector Mark (`aegis_logo.svg`)
The logo mark consists of a geometric shield contour layered with an internal 4-point decision grid, rendered with crisp 1.5px vector strokes in Deep Teal (`#0F5257`).

### Iconography Rules
- **Zero Decorative Emojis:** Never use emojis in UI buttons, CLI outputs, or documentation.
- **Vector SVG Micro-Icons Only:** Use clean 1.5px stroke vector icons for actions (e.g. download, search, filter, view).

---

## 5. UI Component Guidelines

- **Cards:** White surface (`#FFFFFF`), 1px border (`#E2E8F0`), subtle border-color change on hover (`#CBD5E1`). No box shadows or gradients.
- **Buttons:**
  - *Primary:* Solid Deep Teal (`#0F5257`), white text, clean hover state (`#093A3E`).
  - *Secondary / Outline:* Pure white (`#FFFFFF`), border `#E2E8F0`, dark ink text.
- **Radar Charts:** SVG vector lines (`#CBD5E1`) with desaturated teal polygon fill (`rgba(15, 82, 87, 0.15)`).
