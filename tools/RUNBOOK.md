# Reclaivo reel automation runbook
Owner: Abyan. Goal: new Instagram Reels and LinkedIn videos about ONLY influencer marketing agency (IMA) and clipping, posted automatically. Worldwide: never mention any country or the UK.

## Rules (never break)
- Reply starts "Abyan!", never use em or en dashes anywhere (captions, on-screen text, replies), end replies with a separate "Your next task" section.
- Every reel is new: different hook, topic and wording from everything in tools/history.json. Reuse an old reel only if truly out of ideas.
- 1 in 4 reels is a genuine promo for Reclaivo (kind "promo"), realistic, no overselling or overclaiming. Allowed claims: we match brands with creators and help with the deal; we turn a long video into short clips that are ready to post; DM or email us. No fake numbers, no guarantees.
- Max 15 s, 9:16, hook first, voiceover, soft music. Last two lines always: "Comment DEAL/CLIP below." then "Follow, then D M us or email us." (DEAL for influencer topics, CLIP for clipping topics.)
- Captions (long, educational, SEO): 120 to 220 words of real value, not a description of the video. Structure: (1) first line is a keyword-rich title phrase people search for, (2) a short hook sentence, (3) 4 to 6 short lines or numbered tips that teach the topic in practical detail (what to do, why, an example, common mistakes), (4) a one-line takeaway, (5) call to action: "Comment DEAL/CLIP below, then follow and DM us or email hello@reclaivo.com", (6) at most 5 hashtags, SEO relevant. Use plain words people search (influencer marketing, creator partnerships, brand deals, video clipping, short form video, Instagram Reels, LinkedIn). Facts must be accurate and general, no made-up statistics, no guarantees, no country names, no em or en dashes. Promo reels stay honest and low-key and still teach something. Same caption goes to both accounts. Instagram allows 2200 characters, stay under 2000.
- At most 1 in 3 reels uses a 3D insert (kind A or B). Others are plain (kind P).
- TikTok is NOT used (restricted). Only Instagram and LinkedIn.

## Accounts (use the main Zapier connector only, NEVER ZapierP; Publer workspace 6af9e64d1740237b1ce4e8ee, Zapier app App232404CLIAPI, connection hello@reclaivo.com)
- Instagram 6af9e69b1fc93c847bd2b4a8, LinkedIn 6af9f7961740237b1ce51c0a.
- Post to BOTH in ONE create_post call: account_ids = both ids (one Zapier task). Upload each video once (upload_media, one video per call, file_urls = raw GitHub URL, in_library true), reuse the media id.
- state must be "scheduled" (drafts never show). scheduled_at is ISO UTC (UK is UTC+0 in winter, UTC+1 in summer).
- Publer free plan: max 10 scheduled posts per account. If the limit error appears, stop, leave the rest for the next run. Never delete the user's posts.
- Each reel costs 2 Zapier tasks (upload + post). Zapier free plan is 100 tasks a month.

## Cadence
- Until Thu 26 Nov 2026 (Zapier trial): 2 reels per day, 12:00 and 19:00 UK.
- From Fri 27 Nov 2026: 1 reel per day at 19:00 UK, 6 days a week, Sunday is the day off.

## Cover frame
make_week.py already makes frame 0 the designed cover (hook fully shown) via add_cover.sh, so Reels uses it as the thumbnail. Never skip this step; a .cover.png is saved next to each reel.

## Building (Friday 16:30 task)
1. `bash tools/pipeline/setup.sh` (rebuilds the workspace, downloads the voice model from GitHub). Then `pip` and playwright chromium are already present; if not, `python3 -m playwright install chromium`.
2. Read tools/schedule.md and tools/history.json. Work out how many reels are needed to fill every slot from the first unfilled slot through the end of the coming Saturday (cadence above), minus reels already built but unscheduled. Build the shortfall.
3. Invent new reels. Use WebSearch for current news, platform changes and trends in influencer marketing and clipping, but the reel must stay on IMA or clipping only. Make a spec JSON (example: tools/pipeline/specs-week-2.json): per reel k (P/A/B), ad (hook word with ?, max 6 letters), chips (4 x [text, time, x, y, rotation]), L (exactly 7 lines), tag, src, bg (5 of studio, desk, growth, work1, way2, work5), optional slab (e.g. "{3}" index of the highlighted word in line 3 or 4).
   - L[0] hook line; L[1] is the big stamp text and MUST be max 5 words (it collides with the logo pill if longer); keep the whole voiceover 15 s or less, spoken lines must fit 15 s in total. Brand is written "Re clay vee oh" in L (spoken correctly, shown as Reclaivo). "DM" is written "D M".
   - Avoid words the voice skips. make_week.py stops and lists any skipped word (OOV): reword and rerun.
4. `python3 tools/pipeline/make_week.py spec.json /home/claude/out` (use run_in_background, then poll; each 3D reel takes about 10 minutes). It is resumable: if it stops, rerun the same command.
5. Check one frame sheet of every 3D reel (ffmpeg tile) for overlaps, and durations are under 15 s (the script enforces). Fix and rebuild if wrong.
6. Copy finals to reels/<week folder>/NAME.mp4, update tools/history.json (new ids and topics) and tools/schedule.md (status "built"), commit and push (`git -c push.negotiate=true push origin HEAD:main`). Commit messages end with the Co-Authored-By line the session gives.

## Scheduling (done in the same session as the build)
- Read tools/schedule.md. For each built-but-unscheduled reel, in order, upload and create_post to both accounts at the next free slot (cadence). Stop at the 10 limit. Write captions (unique, SEO, rules above). Update tools/schedule.md and push.
- Check with find_media / the create_post result for failures, retry once, report plainly if anything fails.

## Task timing (changed 18 Nov 2026)
There is ONE scheduled task, a one-shot that re-arms itself. It builds and schedules in the same session, then sets its own next run to 16:30 UK two days before the last scheduled slot (tomorrow 10:07 UK if a run failed). No fixed weekly tasks, no separate Saturday or Tuesday checks. If FREE slots (10 minus pending) is 3 or less it skips building and only re-arms.


## New styles (added 17 Nov 2026): Glass Icons and Software Walkthrough
Both are in tools/pipeline/styles/ (examples in reels/examples/). The user approved the look and wants Glass Icons used MORE OFTEN from the next batch, Software Walkthrough occasionally. Data City is NOT used.
- Palette is the Reclaivo palette only: #0B0B0B, lime #DEFB0A, white, greys #cfd2c4 and #9fa391. Keep the top (about 250 px) and bottom (about 450 px) clear: the page content already sits inside a scaled #stage, do not change it.
- Glass Icons: "N things every deal/clip needs" style. 4 icons, each with a card (number, name, one-line benefit). Edit the headline in #hl, the CARD array and the symbols (sym(k)) in glass.html. Lines: hook, 4 beats, Comment DEAL/CLIP below, Follow line.
- Software Walkthrough: 4 click steps in a mock "Deal board" (generic, not a real product). Edit #hl, the NAMES array, TXT (typed message), rows and the 4 beats in walk.html.
- Run: python3 tools/pipeline/styles/make_style.py glass|walk WORKDIR OUT.mp4 (WORKDIR/lines.json holds the 7 spoken lines). It does voice, sound, music, render, compose, cover frame 0 and refuses over 15 s.
- Mix per batch (user wants all styles mixed, 17 Nov): rotate the three styles, 2D template, Glass Icons and Software Walkthrough, roughly a third each, never the same style twice in a row, and match the style to the topic (lists of things = Glass Icons, how-to steps = Software Walkthrough, opinions, mistakes and stories = 2D). Safe zone: all content stays between y 330 and y 1410 of 1920 (already built into the two new pages via #stage scale 0.70); keep 2D reels inside y 330 to 1410 too. Topics stay unique, only IMA and clipping, no made-up stats, no country names. Words missing from the Kokoro lexicon are skipped (OOV list printed): reword them.
