# Multi-school branding plan

This project is moving toward a multi-school SaaS structure. Template branding should be separated from template layout.

## Current rule

Each printable or preview template should treat logo as two separate identities:

1. Main logo
   - Clear, sharp, 100% opacity.
   - Used in header, cards, vouchers and WhatsApp preview image.

2. Watermark logo
   - Large background logo.
   - 20-30% opacity.
   - Used behind document content.

## Current implementation

Reusable CSS file:

```text
static/css/school_logo.css
```

Reusable include:

```text
school/templates/includes/school_logo.html
```

Main logo class:

```html
{% include 'includes/school_logo.html' with logo_class='school-logo-main' %}
```

Watermark logo class:

```html
<div class="print-logo-watermark">
  {% include 'includes/school_logo.html' with logo_class='school-logo-watermark' %}
</div>
```

## Preview behavior

`/template-previews/` uses clickable demo logos. Clicking the front logo cycles brand colors to simulate school/tenant branding.

## Future SaaS fields

When multi-school support is added, create a `SchoolTenant` or `CampusProfile` model with fields like:

```text
school_name
campus_code
address
phone
email
main_logo
watermark_logo
primary_color
secondary_color
accent_color
```

Then templates should read:

```django
{{ active_school.school_name }}
{{ active_school.main_logo.url }}
{{ active_school.watermark_logo.url }}
```

CSS variables should be generated from tenant colors:

```css
:root {
  --school-primary: {{ active_school.primary_color }};
  --school-secondary: {{ active_school.secondary_color }};
  --school-accent: {{ active_school.accent_color }};
}
```

## Design principle

Do not hardcode school-specific logo, colors, address or phone in every template. Keep layout reusable and load school branding from one active tenant profile.
