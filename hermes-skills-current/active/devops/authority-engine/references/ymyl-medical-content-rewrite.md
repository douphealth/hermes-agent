# YMYL Medical Content Rewrite — Safety-First Enterprise Pattern

Use this when rewriting health/medical diagnosis, treatment, or symptom content on a public WordPress site. Medical content can cause real-world harm if published with errors — this pattern prioritizes safety, accuracy, and expert review over speed.

## 1. Safety-first: Noindex before touching

**Before any rewrite, noindex the page immediately.**

Rationale: The live page may contain inaccurate medical information (e.g., "2026 McDonald criteria" — only 2024 revision exists as of writing; or the current valid revision is 2017). A reader seeing this before the fix is a liability.

```bash
# Via Yoast REST or meta_input
curl -sS -X POST "https://example.com/wp-json/wp/v2/posts/{ID}" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -H "X-HTTP-Method-Override: PUT" \
  --data-binary '{"meta": {"_yoast_wpseo_meta-robots-noindex": "1", "_yoast_wpseo_meta-robots-adv": "none"}}'
```

If Yoast meta isn't REST-writable, use a Code Snippets `wp_robots` filter as fallback:
```php
add_filter('wp_robots', function($robots, $path = '') {
    if (stripos($_SERVER['REQUEST_URI'] ?? '', '/health/multiple-sclerosis-diagnosis') !== false) {
        $robots['noindex'] = true;
        $robots['follow'] = true;
    }
    return $robots;
}, 999, 2);
```

The page stays noindexed until the rewrite is verified accurate and the expert review is in place.

## 2. Named expert reviewer requirement

For YMYL medical content, generic placeholders like "Medical reviewer: [Insert real neurologist]" are unacceptable.

**Required pattern:**
- **Name a real, identifiable expert** (e.g., "Dr. Jane Smith, MD, FAAN — Board-Certified Neurologist")
- Include their credentials, institution/affiliation, and specialization area
- Add a brief bio/qualification note
- Verify the named expert is real (affiliated with a legitimate medical institution)
- Include their review date

**Do NOT:**
- Use "Expert Reviewed" or "Certified [Profession]" without a verified real person
- Fabricate reviewer names or credentials
- Use vague language like "our medical team" without naming the reviewer
- Use AI-generated "Dr. [Name]" placeholders

The user's preference: "named neurologist/MS reviewer" is the minimum bar. If you cannot name one, flag it as a blocker rather than publishing without one.

## 3. Diagnostic criteria accuracy — no invented future revisions

Medical guidelines and diagnostic criteria have specific revision cycles. Never reference unreleased future versions.

**Example failure:** "2026 McDonald criteria" — no such thing exists. Only refer to criteria by their actual published revision year (currently the 2017 revision for McDonald criteria; ICD-11 is the current disease classification).

**Checklist before publishing medical facts:**
- [ ] Is the guideline/criteria version the latest published?
- [ ] Are we citing the correct revision year?
- [ ] Have we avoided speculating about future revisions?
- [ ] Are diagnostic criteria quoted accurately (not summarized loosely)?
- [ ] Is the source of the criteria cited (e.g., "Thompson AJ, et al. Lancet Neurol. 2018")?

## 4. Recommended structure for diagnosis/condition content

For a diagnosis-focused medical article (user's requested angle: "How MS Is Diagnosed: Symptoms, MRI, Lumbar Puncture, McDonald Criteria, and What to Ask Your Neurologist"), structure as:

### Title & H1
- Use the "How MS Is Diagnosed: …" pattern (not "Early MS Diagnosis: 7 Signs…")
- Include the diagnostic method keyword and the patient-advocacy angle
- Example: "How MS Is Diagnosed: Symptoms, MRI, Lumbar Puncture, McDonald Criteria, and What to Ask Your Neurologist"

### Intro
- Answer-first: directly state how MS is diagnosed (no single test, combination of clinical exam + MRI + LP + evoked potentials using McDonald criteria)
- Include the named expert reviewer + review date prominently
- Set expectations: this is an educational overview, not a substitute for professional medical advice

### Sections to include (in order):
1. **Overview of the Diagnostic Process** — no single test, combination approach
2. **Clinical Presentation — Recognizing MS Symptoms** — common presenting symptoms (optic neuritis, sensory changes, motor weakness, Lhermitte sign, Uhthoff phenomenon)
3. **Neurological Examination** — what the neurologist checks (reflexes, coordination, gait, cranial nerves)
4. **MRI — The Most Important Diagnostic Tool** — brain and spinal cord MRI, T2 hyperintense lesions, contrast-enhanced gadolinium lesions, dissemination in space and time
5. **Lumbar Puncture (Spinal Tap)** — CSF analysis for oligoclonal bands (OCBs), IgG index, protein levels
6. **Evoked Potentials** — visual evoked potentials (VEP), somatosensory evoked potentials (SSEP)
7. **Blood Tests — Ruling Out Mimics** — vitamin B12, thyroid, autoimmune panels (ANA, anti-dsDNA), Lyme, syphilis, HIV
8. **The McDonald Criteria — Current (2017) Revision** — explain DIS and DIT, what has changed from previous revisions, what (if any) proposed revisions are in the pipeline
9. **What to Ask Your Neurologist** — patient-advocacy section with actionable questions:
   - "Do I meet McDonald criteria for a diagnosis of MS?"
   - "What type of MS do I have?"
   - "Do I need a lumbar puncture, or can diagnosis be made based on MRI alone?"
   - "Are there other conditions that could explain my symptoms?"
   - "Should I see an MS specialist?"
   - "What is my lesion burden and where are the lesions located?"
10. **FAQ** — common questions (how long does diagnosis take, can you have MS with a normal MRI, is MS hereditary, etc.)
11. **References** — DOI-formatted citations to peer-reviewed literature

### Elements to include:
- [ ] Medical disclaimer (YMYL-compliant, prominent)
- [ ] Named expert reviewer block
- [ ] "When to see a doctor" guidance
- [ ] "What to ask your neurologist" patient-advocacy section
- [ ] Diagnostic criteria accuracy note (cite the exact revision)
- [ ] Conditions that mimic MS (differential diagnosis)
- [ ] FAQ
- [ ] References with DOIs
- [ ] Schema markup (Article, MedicalWebPage or similar if Yoast supports it)
- [ ] Internal links to related health content on the site (symptom guides, related conditions)
- [ ] Freshness signal (last reviewed/updated date)

## 5. Medical disclaimer standards

The disclaimer must be:
- **Visible** — not buried in a thin footer. Use a prominent callout box near the top or in a sitewide notice area.
- **Explicit** — "This content is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition."
- **Linked** to a full editorial/disclaimer policy page

## 6. Rewrite workflow

1. **Noindex** the page (immediately — first action)
2. **Read** the existing post (full REST `context=edit` to see raw content)
3. **Assess** what's wrong: inaccurate criteria, missing sections, weak trust signals, generic tone
4. **Plan** the rewrite using the structure above
5. **Draft** with the named expert reviewer (flag if no real name is available)
6. **Push** via REST with `X-HTTP-Method-Override: PUT`
7. **Set Yoast metadata** (title, description, noindex still active)
8. **Verify** live page — check body, H1, disclaimers, schema, internal links
9. **Purge** Cloudflare/LiteSpeed cache
10. **Verify again** on cache-busted URL
11. **Only then** remove noindex and re-verify

## 7. Pitfalls

- **Fake expert names** — The user will catch AI-generated reviewer names instantly. Use only real, verified experts.
- **Inventing future criteria** — Never write "2026 McDonald criteria" or similar. If no revision has been announced, say "the current 2017 revision" and note any proposed changes as speculative.
- **Overstating diagnostic certainty** — MS diagnosis requires clinical judgment; no single test is definitive. Always include the differential diagnosis.
- **Treatment claims on a diagnosis page** — This is a DIAGNOSIS page. Keep treatment information minimal unless explicitly requested. If included, separate it clearly and maintain YMYL standards.
- **Missing lumbar puncture explanation** — Many readers fear the LP. Explain why it matters and what it feels like (common anxiety driver).
- **The "What to Ask" section is not optional** — This is the user's requested angle and adds patient-advocacy value. Skip it and the page looks like generic medical content.
- **Noindex removal timing** — Do not remove noindex until the expert reviewer block is verified in the live HTML, all diagnostic accuracy checks pass, and the page returns 200 with the correct H1 and disclaimers.
