<script>
  /**
   * @typedef {Object} Position
   * @property {number} id
   * @property {string} code
   * @property {string} name
   * @property {string | null} description
   */

  /**
   * @typedef {Object} Lesson
   * @property {number} id
   * @property {number} position_id
   * @property {string} title
   * @property {string | null} description
   * @property {number} step_order
   * @property {boolean} is_active
   */

  export let API_URL = "";
  export let canManageLessons = false;

  /** @type {Position | null} */
  export let selectedPosition = null;

  /** @type {Lesson[]} */
  export let lessons = [];

  /** @type {() => void} */
  export let onDataChanged = () => {};

  let isReaderOpen = false;
  let currentIndex = 0;

  /** @type {Lesson[]} */
  $: sortedLessons = [...lessons].sort((a, b) => a.step_order - b.step_order);

  /** @type {Lesson | null} */
  $: currentLesson = sortedLessons[currentIndex] || null;

  $: progressPercent =
    sortedLessons.length > 0 ? ((currentIndex + 1) / sortedLessons.length) * 100 : 0;

  /**
   * @param {number} index
   */
  function openLesson(index) {
    currentIndex = index;
    isReaderOpen = true;
  }

  function closeReader() {
    isReaderOpen = false;
  }

  function nextLesson() {
    if (currentIndex < sortedLessons.length - 1) {
      currentIndex += 1;
    }
  }

  function previousLesson() {
    if (currentIndex > 0) {
      currentIndex -= 1;
    }
  }

  /**
   * @param {string | null} text
   * @returns {string[]}
   */
  function splitContent(text) {
    if (!text) return [];

    return text
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);
  }

  /**
   * @param {string} line
   * @returns {"heading" | "formula" | "script" | "warning" | "checklist" | "normal"}
   */
  function getLineType(line) {
    if (/^\d+\./.test(line)) return "heading";

    if (line.includes("=")) return "formula";

    if (
      line.includes("ตัวอย่าง") ||
      line.includes("วิธีพูด") ||
      line.includes("สคริปต์") ||
      line.includes("Script") ||
      line.includes("Sales Script")
    ) {
      return "script";
    }

    if (
      line.includes("ห้าม") ||
      line.includes("ไม่ควร") ||
      line.includes("ข้อควรระวัง") ||
      line.includes("ระวัง")
    ) {
      return "warning";
    }

    if (
      line.includes("จุดที่ต้องจำ") ||
      line.includes("Checklist") ||
      line.includes("สิ่งที่พนักงานต้องจำ")
    ) {
      return "checklist";
    }

    return "normal";
  }

  /**
   * @param {Lesson} lesson
   */
  async function editLesson(lesson) {
    const newTitle = prompt("แก้ชื่อบทเรียน", lesson.title);
    if (newTitle === null) return;

    const newDescription = prompt("แก้รายละเอียดบทเรียน", lesson.description || "");
    if (newDescription === null) return;

    const newStepOrderText = prompt("แก้ลำดับ Step", String(lesson.step_order));
    if (newStepOrderText === null) return;

    const response = await fetch(`${API_URL}/lessons/${lesson.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title: newTitle,
        description: newDescription,
        step_order: Number(newStepOrderText)
      })
    });

    if (response.ok) {
      alert("แก้ไขบทเรียนสำเร็จ");
      onDataChanged();
    } else {
      alert("แก้ไขบทเรียนไม่สำเร็จ");
    }
  }

  /**
   * @param {Lesson} lesson
   */
  async function deleteLesson(lesson) {
    const confirmed = confirm(`ต้องการลบบทเรียน "${lesson.title}" ใช่ไหม?`);
    if (!confirmed) return;

    const response = await fetch(`${API_URL}/lessons/${lesson.id}`, {
      method: "DELETE"
    });

    if (response.ok) {
      alert("ลบบทเรียนสำเร็จ");
      onDataChanged();
    } else {
      alert("ลบบทเรียนไม่สำเร็จ");
    }
  }
</script>

{#if selectedPosition}
  <section class="training-zone">
    <div class="academy-header">
      <div>
        <span class="academy-kicker">Training Quest</span>
        <h2>{selectedPosition.name}</h2>
        <p>
          เลือก Mission เพื่อเข้าเรียนทีละ Step ระบบนี้ออกแบบให้พนักงานใหม่เรียนเหมือนเดินด่านในเกม
          พร้อม Progress และปุ่ม Next Lesson
        </p>
      </div>

      <div class="level-badge">
        <span>Role</span>
        <strong>{selectedPosition.code}</strong>
      </div>
    </div>

    {#if sortedLessons.length === 0}
      <div class="empty-training">
        <div class="empty-icon">◇</div>
        <h3>ยังไม่มีบทเรียนของตำแหน่งนี้</h3>
        <p>เพิ่มบทเรียนจากหน้า Admin ก่อน แล้วกลับมาเริ่ม Training Quest</p>
      </div>
    {:else}
      <div class="quest-map">
        {#each sortedLessons as lesson, index}
          <article class="quest-card">
            <div class="quest-top">
              <div class="step-orb">
                <span>{String(lesson.step_order).padStart(2, "0")}</span>
              </div>

              <div class="quest-status">
                {#if index === 0}
                  Starter
                {:else if index === sortedLessons.length - 1}
                  Final
                {:else}
                  Mission
                {/if}
              </div>
            </div>

            <div class="quest-body">
              <span class="mission-label">Mission {String(index + 1).padStart(2, "0")}</span>
              <h3>{lesson.title}</h3>
              <p>
                {lesson.description
                  ? lesson.description.slice(0, 135) + (lesson.description.length > 135 ? "..." : "")
                  : "ยังไม่มีรายละเอียดบทเรียน"}
              </p>
            </div>

            <div class="quest-actions">
              <button type="button" on:click={() => openLesson(index)}>
                Start Lesson
              </button>

              {#if canManageLessons}
                <button
                  type="button"
                  class="secondary-button"
                  on:click={() => editLesson(lesson)}
                >
                  Edit
                </button>

                <button
                  type="button"
                  class="danger-button"
                  on:click={() => deleteLesson(lesson)}
                >
                  Delete
                </button>
              {/if}
            </div>
          </article>
        {/each}
      </div>
    {/if}
  </section>
{:else}
  <section class="training-zone">
    <div class="empty-training">
      <div class="empty-icon">◇</div>
      <h3>ยังไม่ได้เลือก Position</h3>
      <p>กรุณาเลือก Position จากหน้า Access Login ก่อนเข้าสู่ Training Quest</p>
    </div>
  </section>
{/if}

{#if isReaderOpen && currentLesson}
  <section class="reader-overlay">
    <div class="reader-shell">
      <aside class="reader-sidebar">
        <button type="button" class="close-button" on:click={closeReader}>
          Close
        </button>

        <div class="reader-role">
          <span>Current Role</span>
          <strong>{selectedPosition?.name}</strong>
        </div>

        <div class="progress-box">
          <div class="progress-text">
            <span>Progress</span>
            <strong>Step {currentIndex + 1} / {sortedLessons.length}</strong>
          </div>

          <div class="progress-track">
            <div class="progress-fill" style={`width: ${progressPercent}%`}></div>
          </div>
        </div>

        <div class="mini-map">
          {#each sortedLessons as lesson, index}
            <button
              type="button"
              class:active={index === currentIndex}
              on:click={() => openLesson(index)}
            >
              <span>{String(index + 1).padStart(2, "0")}</span>
              {lesson.title}
            </button>
          {/each}
        </div>
      </aside>

      <main class="lesson-reader">
        <div class="lesson-hero">
          <span>Mission {String(currentIndex + 1).padStart(2, "0")}</span>
          <h1>{currentLesson.title}</h1>
          <p>
            อ่านบทเรียนนี้ให้เข้าใจ แล้วกด Next Lesson เพื่อไปยังด่านถัดไป
          </p>
        </div>

        <div class="lesson-content">
          {#each splitContent(currentLesson.description) as line}
            {#if getLineType(line) === "heading"}
              <h2>{line}</h2>
            {:else if getLineType(line) === "formula"}
              <div class="content-block formula-block">
                {line}
              </div>
            {:else if getLineType(line) === "script"}
              <div class="content-block script-block">
                {line}
              </div>
            {:else if getLineType(line) === "warning"}
              <div class="content-block warning-block">
                {line}
              </div>
            {:else if getLineType(line) === "checklist"}
              <div class="content-block checklist-block">
                {line}
              </div>
            {:else}
              <p>{line}</p>
            {/if}
          {/each}
        </div>

        <div class="reader-nav">
          <button
            type="button"
            class="secondary-button"
            disabled={currentIndex === 0}
            on:click={previousLesson}
          >
            Previous
          </button>

          <div class="reader-nav-center">
            <span>{currentIndex + 1}</span>
            <p>of {sortedLessons.length}</p>
          </div>

          <button
            type="button"
            disabled={currentIndex === sortedLessons.length - 1}
            on:click={nextLesson}
          >
            Next Lesson
          </button>
        </div>
      </main>
    </div>
  </section>
{/if}

<style>
  .training-zone {
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(246, 244, 240, 0.92));
    border: 1px solid rgba(20, 20, 20, 0.08);
    border-radius: 32px;
    padding: clamp(24px, 3vw, 34px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.07);
  }

  .academy-header {
    display: flex;
    justify-content: space-between;
    gap: 22px;
    align-items: flex-start;
    margin-bottom: 28px;
  }

  .academy-kicker {
    display: block;
    color: #5f1d2b;
    font-weight: 800;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    font-size: 12px;
    margin-bottom: 8px;
  }

  .academy-header h2 {
    margin: 0 0 10px;
    font-size: clamp(32px, 4vw, 52px);
    line-height: 1.05;
    font-weight: 500;
  }

  .academy-header p {
    margin: 0;
    max-width: 760px;
    color: #6f655d;
    line-height: 1.8;
  }

  .level-badge {
    flex: 0 0 auto;
    min-width: 150px;
    padding: 18px;
    border-radius: 24px;
    background: #111;
    color: white;
    text-align: center;
    box-shadow: 0 18px 42px rgba(0, 0, 0, 0.18);
  }

  .level-badge span {
    display: block;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: rgba(255, 255, 255, 0.62);
    margin-bottom: 8px;
  }

  .level-badge strong {
    font-size: 24px;
  }

  .quest-map {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 22px;
  }

  .quest-card {
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    background:
      radial-gradient(circle at top right, rgba(95, 29, 43, 0.08), transparent 30%),
      linear-gradient(135deg, #ffffff, #f7f4ef);
    border: 1px solid rgba(20, 20, 20, 0.08);
    padding: 22px;
    min-height: 310px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.07);
    transition: 0.22s ease;
  }

  .quest-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 28px 80px rgba(0, 0, 0, 0.12);
  }

  .quest-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
      linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.7) 42%, transparent 70%);
    transform: translateX(-100%);
    transition: 0.5s ease;
    pointer-events: none;
  }

  .quest-card:hover::before {
    transform: translateX(100%);
  }

  .quest-top {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
  }

  .step-orb {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    background: #111;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 18px 36px rgba(0, 0, 0, 0.18);
  }

  .step-orb span {
    font-size: 20px;
    font-weight: 800;
  }

  .quest-status {
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(95, 29, 43, 0.08);
    color: #5f1d2b;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }

  .quest-body {
    position: relative;
    z-index: 2;
    flex: 1;
  }

  .mission-label {
    display: block;
    color: #5f1d2b;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .quest-body h3 {
    margin: 0 0 12px;
    font-size: clamp(24px, 2.5vw, 34px);
    line-height: 1.1;
  }

  .quest-body p {
    color: #6f655d;
    line-height: 1.75;
  }

  .quest-actions {
    position: relative;
    z-index: 2;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 22px;
  }

  .quest-actions button {
    margin: 0;
  }

  .empty-training {
    text-align: center;
    padding: 60px 20px;
    border-radius: 28px;
    background: rgba(255, 255, 255, 0.68);
    border: 1px dashed rgba(20, 20, 20, 0.15);
  }

  .empty-icon {
    font-size: 64px;
    color: #5f1d2b;
  }

  .empty-training h3 {
    margin: 10px 0;
    font-size: 28px;
  }

  .empty-training p {
    color: #6f655d;
  }

  .reader-overlay {
    position: fixed;
    inset: 0;
    z-index: 999;
    background: rgba(8, 8, 8, 0.72);
    backdrop-filter: blur(16px);
    padding: 24px;
    overflow: auto;
  }

  .reader-shell {
    max-width: 1360px;
    min-height: calc(100vh - 48px);
    margin: 0 auto;
    display: grid;
    grid-template-columns: 320px minmax(0, 1fr);
    background: #f6f3ef;
    border-radius: 34px;
    overflow: hidden;
    box-shadow: 0 30px 100px rgba(0, 0, 0, 0.34);
  }

  .reader-sidebar {
    background: #111;
    color: white;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 22px;
  }

  .close-button {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    align-self: flex-start;
  }

  .close-button:hover {
    background: white;
    color: #111;
  }

  .reader-role span,
  .progress-text span {
    display: block;
    color: rgba(255, 255, 255, 0.58);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
  }

  .reader-role strong {
    font-size: 24px;
    line-height: 1.2;
  }

  .progress-box {
    padding: 18px;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.08);
  }

  .progress-text {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
  }

  .progress-text strong {
    color: #fff;
  }

  .progress-track {
    height: 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.12);
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    border-radius: 999px;
    background: #fff;
    transition: width 0.25s ease;
  }

  .mini-map {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .mini-map button {
    width: 100%;
    text-align: left;
    background: rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.76);
    border-radius: 16px;
    box-shadow: none;
    margin: 0;
    line-height: 1.45;
  }

  .mini-map button.active,
  .mini-map button:hover {
    background: #fff;
    color: #111;
  }

  .mini-map button span {
    display: inline-flex;
    margin-right: 8px;
    font-weight: 800;
    color: #5f1d2b;
  }

  .lesson-reader {
    padding: clamp(28px, 4vw, 54px);
    overflow: auto;
  }

  .lesson-hero {
    margin-bottom: 32px;
    padding-bottom: 28px;
    border-bottom: 1px solid rgba(20, 20, 20, 0.08);
  }

  .lesson-hero span {
    display: block;
    color: #5f1d2b;
    font-weight: 800;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    font-size: 12px;
    margin-bottom: 10px;
  }

  .lesson-hero h1 {
    margin: 0 0 16px;
    font-size: clamp(38px, 5vw, 72px);
    line-height: 1;
  }

  .lesson-hero p {
    max-width: 780px;
    color: #6f655d;
    line-height: 1.8;
  }

  .lesson-content {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .lesson-content h2 {
    margin: 22px 0 4px;
    font-size: clamp(26px, 3vw, 42px);
    color: #111;
  }

  .lesson-content p {
    font-size: 17px;
    line-height: 1.9;
    color: #413b36;
    background: rgba(255, 255, 255, 0.58);
    border: 1px solid rgba(20, 20, 20, 0.05);
    border-radius: 18px;
    padding: 16px 18px;
  }

  .content-block {
    border-radius: 20px;
    padding: 18px 20px;
    line-height: 1.85;
    font-size: 17px;
  }

  .formula-block {
    background: #111;
    color: #fff;
  }

  .script-block {
    background: rgba(95, 29, 43, 0.08);
    border: 1px solid rgba(95, 29, 43, 0.12);
    color: #3a2027;
  }

  .warning-block {
    background: rgba(142, 43, 43, 0.1);
    border: 1px solid rgba(142, 43, 43, 0.15);
    color: #6f1f1f;
  }

  .checklist-block {
    background: rgba(17, 17, 17, 0.06);
    border: 1px solid rgba(17, 17, 17, 0.1);
    color: #111;
    font-weight: 700;
  }

  .reader-nav {
    margin-top: 34px;
    padding-top: 24px;
    border-top: 1px solid rgba(20, 20, 20, 0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
  }

  .reader-nav button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    transform: none;
  }

  .reader-nav-center {
    text-align: center;
  }

  .reader-nav-center span {
    display: block;
    font-size: 28px;
    font-family: Georgia, serif;
  }

  .reader-nav-center p {
    margin: 0;
    color: #6f655d;
  }

  @media (max-width: 980px) {
    .academy-header {
      flex-direction: column;
    }

    .reader-shell {
      grid-template-columns: 1fr;
    }

    .reader-sidebar {
      position: relative;
    }
  }

  @media (max-width: 640px) {
    .reader-overlay {
      padding: 10px;
    }

    .reader-shell {
      border-radius: 24px;
    }

    .lesson-reader {
      padding: 24px;
    }

    .reader-nav {
      flex-direction: column;
    }

    .reader-nav button {
      width: 100%;
    }
  }
</style>