# Social Content Method Selection Smoke

Use this as a text smoke fixture for method routing.

## Positive Cases

| Input | Expected method | Why |
| --- | --- | --- |
| "Create a 7-slide Instagram carousel explaining the product launch." | `social-content:carousel` | Multi-slide social artifact is primary. |
| "Write a founder LinkedIn post about our hiring push." | `social-content:linkedin` | Professional LinkedIn voice and context drive the method. |
| "Turn this essay into an X thread with a strong hook." | `social-content:twitter-thread` | Thread structure and standalone tweet logic are primary. |
| "Plan a TikTok, Instagram, Shorts, and X launch bundle." | `social-content:cross-platform` | Multi-platform adaptation and campaign bundle are primary. |

## Supporting Method Cases

| Input | Primary | Supporting | Why |
| --- | --- | --- | --- |
| "Make a LinkedIn carousel for a founder POV." | `social-content:carousel` | `social-content:linkedin` | Carousel owns artifact structure; LinkedIn owns voice and platform norms. |
| "Create a cross-platform launch with a thread and carousel." | `social-content:cross-platform` | `social-content:carousel`, `social-content:twitter-thread` | Campaign owns the bundle; artifact methods support subformats. |

## Negative Controls

- Do not choose `social-content:carousel` for a single image caption.
- Do not choose `social-content:twitter-thread` for generic multi-platform
  caption sets.
- Do not imply publish, schedule, comment, DM, or cross-post permission unless
  the user explicitly asks for that action.
