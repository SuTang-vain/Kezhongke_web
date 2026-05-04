---
name: Liquid Humanism
colors:
  surface: '#fff8f6'
  surface-dim: '#eed4cf'
  surface-bright: '#fff8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff0ed'
  surface-container: '#ffe9e4'
  surface-container-high: '#fde2dd'
  surface-container-highest: '#f7ddd7'
  on-surface: '#261815'
  on-surface-variant: '#5a413b'
  inverse-surface: '#3c2d29'
  inverse-on-surface: '#ffede9'
  outline: '#8e706a'
  outline-variant: '#e2bfb7'
  surface-tint: '#b02e10'
  primary: '#ad2c0d'
  on-primary: '#ffffff'
  primary-container: '#cf4425'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb4a3'
  secondary: '#3e6659'
  on-secondary: '#ffffff'
  secondary-container: '#c0ecdc'
  on-secondary-container: '#446c5f'
  tertiary: '#5c5977'
  on-tertiary: '#ffffff'
  tertiary-container: '#747191'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad2'
  primary-fixed-dim: '#ffb4a3'
  on-primary-fixed: '#3d0600'
  on-primary-fixed-variant: '#8b1a00'
  secondary-fixed: '#c0ecdc'
  secondary-fixed-dim: '#a5d0c0'
  on-secondary-fixed: '#002018'
  on-secondary-fixed-variant: '#264e42'
  tertiary-fixed: '#e4dfff'
  tertiary-fixed-dim: '#c7c2e6'
  on-tertiary-fixed: '#1b1833'
  on-tertiary-fixed-variant: '#464361'
  background: '#fff8f6'
  on-background: '#261815'
  surface-variant: '#f7ddd7'
typography:
  display-hero:
    fontFamily: Source Han Serif SC
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Source Han Serif SC
    fontSize: 40px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Source Han Serif SC
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
  glass-padding: 32px
---

## Brand & Style

This design system is built upon the "Liquid Glass" aesthetic, a forward-looking evolution of Glassmorphism that emphasizes organic fluidity and high-precision optics. The brand personality is scholarly yet cutting-edge, blending the warmth of traditional Chinese humanism with the crystalline clarity of future technology.

The visual direction utilizes heavy backdrop blurs, dynamic caustic light effects, and a "wet" surface tension across all UI elements. It evokes a sense of calm, intellectual depth, and premium craftsmanship, specifically designed to appeal to an audience that values both heritage and innovation.

## Colors

The palette centers on **Soft Amber (#D94B2B)**, used sparingly for call-to-actions and brand marks to maintain a sophisticated scholarly tone. The foundation is built on **Paper White** and **Warm White**, providing a tactile, non-glare canvas that feels more organic than digital pure white.

Secondary accents—**Pale Teal, Soft Mint, and Lavender**—are used as "liquid spills" behind glass surfaces. These colors should never be fully opaque; they exist as blurred blobs or soft gradients that shift subtly as the user scrolls, creating the "liquid" refraction effect characteristic of this design system.

## Typography

This design system employs a sophisticated dual-type strategy. **Source Han Serif (Songti style)** is used for primary titles and headlines to ground the brand in Chinese intellectual tradition. Its high-contrast strokes provide a "humanistic" counterpoint to the high-tech UI.

For functional text and body copy, **Inter** (as a proxy for SF Pro) provides maximum legibility and a modern, systematic feel. High-precision kerning and generous line heights are essential to maintain the "breathable" quality of the layout. Headlines should utilize a slightly condensed letter spacing to appear more intentional and premium.

## Layout & Spacing

The layout philosophy follows a **fixed-center grid** for desktop and a **fluid safe-area grid** for mobile. A 12-column system is used with generous gutters to allow the "liquid" background elements to peek through between content modules.

Spacing rhythm is strictly based on an 8px scale. However, internal padding within glass containers should be exceptionally large (min 32px) to reinforce the sense of weightlessness and light. Negative space is treated as a physical material, used to separate distinct "vessels" of information.

## Elevation & Depth

Depth is achieved through **multi-layered refraction** rather than traditional drop shadows. This design system utilizes three distinct layers of elevation:

1.  **The Caustic Base:** The bottom-most layer containing soft, shifting gradients of Teal and Lavender.
2.  **The Frosted Vessel:** Glass cards with a `backdrop-filter: blur(40px)` and a thin, 1px semi-transparent white border (0.2 opacity) that simulates a light-catching edge.
3.  **Floating Elements:** Interactive components (buttons, active tags) that use a highly diffused, low-opacity shadow tinted with the primary Amber color (#D94B2B at 10% opacity) to suggest they are hovering just above the glass.

The "Liquid" feel is finalized with a subtle inner glow on glass cards to simulate the thickness of high-quality crystal.

## Shapes

The shape language is defined by **super-ellipses (squivcles)**. Standard rectangles are strictly avoided. All glass containers must feature a corner radius of 24px or higher to maintain the "liquid drop" aesthetic.

Buttons and chips adopt a full pill-shape (100px) to contrast against the larger, softer curves of the containers. All "inner" elements within a card should have a radius that is exactly half of the parent container's radius to ensure visual nesting harmony.

## Components

### Glass Cards
The signature component. These must have a `saturate(180%)` and `blur(40px)` background filter. The border should be a linear gradient (top-left to bottom-right) from `rgba(255,255,255,0.4)` to `rgba(255,255,255,0.1)`.

### Liquid Buttons
Primary buttons use a solid Soft Amber fill with a subtle "inner liquid" glow. On hover, the button should expand slightly (scale 1.02) and the internal gradient should shift as if reacting to gravity.

### Input Fields
Inputs are treated as "etched" surfaces—slightly darker than the glass they sit on, with a subtle inner shadow to indicate depth. The focus state is marked by a Soft Amber glow that bleeds into the surrounding glass.

### Navigation
The navigation bar should be a "Floating Island" design, detached from the top of the viewport, featuring the same high-blur glass effect and a micro-interaction where the background blur intensifies upon scrolling.

### Icons
Line-based icons with a 1.5pt stroke weight. Key terminals in the icon design should be rounded to match the typography. Occasional "dual-tone" fills using the Soft Mint and Pale Teal palette can be used for illustrative icons.