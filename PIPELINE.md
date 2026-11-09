# CertsClub Instagram pipeline

1. **Research** each exam code in `queue.txt` on the vendor's official certification page: questions, duration, price, level, official domain weights. Skip retired exams and note them in posted.txt.
2. **Write** `tools/posts/<code-lowercase>.json` in the same shape as the existing files: vendor, name, code, hook, facts (Questions/Time/Price/Level), domains [[name, "NN%"]...] (max 10, short names, use official weights), tips (4, last one = "Take timed practice tests with explanations"), caption.
   Caption format (keep it): "Planning to take the <VENDOR> <CODE> – <Name> exam? 🚀" / "📌 <q> questions · <time> · <price>" / "📚 Biggest topics: <top 3>" / "Swipe through for the full exam breakdown and a study plan 👉" / "Practice with real exam-style <CODE> questions and detailed explanations at www.certsclub.com" / "💾 Save this post for your prep and share it with someone studying <VENDOR>!" / 5 topic hashtags + vendor hashtags + "#ITCertification #CertsClub #PracticeExam #ExamPrep".
3. **Render**: `python3 tools/render.py tools/posts/<code>.json <vendor-lower>/<code> random` (styles navy/split/card rotate at random; no logo; www.certsclub.com only on the last slide). View every slide and fix overflow/typos before publishing.
4. **Push** the slides to this repo (main). Public URL: `https://raw.githubusercontent.com/LumiHill1/certsclub-media1/main/<vendor>/<code>/slideN.jpg`.
5. **Schedule** in Metricool (brand CertsClub, blogId 7183929, Instagram @wyattdylan222) as a 5-image carousel POST, autoPublish true, at 10:00 Asia/Karachi, one per day, starting the day after the latest already-scheduled post.
6. Move the code from `queue.txt` to `posted.txt` with its date, commit and push.
