# Video Production Method Selection Smoke

Use this as a text smoke fixture for video method routing.

## Positive Cases

| Input | Expected method | Why |
| --- | --- | --- |
| "Create a launch promo for our new product." | `video-production:marketing` | Campaign creative and promo story are primary. |
| "Make a 60-second how-it-works video with narration." | `video-production:explainer` | Explanation structure and narration are primary. |
| "Plan the shot list and panels before we generate clips." | `video-production:storyboard` | Visual script and continuity planning are primary. |
| "Make an AI presenter clip from this script." | `video-production:talking-head` | Presenter, voice, likeness, and portrait behavior are primary. |
| "Create a TikTok ad spec with safe zones and captions." | `video-production:ad-spec` | Platform delivery constraints are primary. |

## Supporting Method Cases

| Input | Primary | Supporting | Why |
| --- | --- | --- | --- |
| "Product explainer plus TikTok cutdown." | `video-production:explainer` | `video-production:ad-spec` | Explainer owns story; ad-spec owns platform cutdown. |
| "UGC ad with storyboard before generation." | `video-production:marketing` | `video-production:storyboard` | Marketing owns campaign job; storyboard owns pre-generation panels. |

## Negative Controls

- Do not choose `video-production:ad-spec` for a generic brand story unless
  platform placement specs are required.
- Do not choose `video-production:talking-head` unless a presenter/avatar/
  portrait/likeness constraint is central.
- Do not imply publish, upload, media spend, or likeness approval unless the
  user explicitly authorizes it.
