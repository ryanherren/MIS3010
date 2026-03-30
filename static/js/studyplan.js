(function () {
    "use strict";

    const STORAGE_ITEMS = "studyplan_items_v1";
    const STORAGE_BLOCKS = "studyplan_work_blocks_v1";
    const STORAGE_GRADES = "studyplan_grades_v1";
    const PRIORITY_ORDER = { HIGH: 0, MEDIUM: 1, LOW: 2 };

    function uid() {
        return "sp_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 9);
    }

    function getItems() {
        try {
            const raw = localStorage.getItem(STORAGE_ITEMS);
            const arr = raw ? JSON.parse(raw) : [];
            return Array.isArray(arr) ? arr : [];
        } catch {
            return [];
        }
    }

    function saveItems(items) {
        localStorage.setItem(STORAGE_ITEMS, JSON.stringify(items));
        window.dispatchEvent(new CustomEvent("studyplan:itemschanged"));
    }

    function getBlocks() {
        try {
            const raw = localStorage.getItem(STORAGE_BLOCKS);
            const arr = raw ? JSON.parse(raw) : [];
            return Array.isArray(arr) ? arr : [];
        } catch {
            return [];
        }
    }

    function saveBlocks(blocks) {
        localStorage.setItem(STORAGE_BLOCKS, JSON.stringify(blocks));
        window.dispatchEvent(new CustomEvent("studyplan:blockschanged"));
    }

    function timeToMinutes(t) {
        if (!t || typeof t !== "string") return NaN;
        const p = t.trim().split(":");
        const h = parseInt(p[0], 10);
        const m = parseInt(p[1] ?? "0", 10);
        if (isNaN(h) || isNaN(m)) return NaN;
        return h * 60 + m;
    }

    function minutesToTime(mins) {
        const h = Math.floor(mins / 60);
        const m = mins % 60;
        return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
    }

    function formatBlockDuration(startTime, endTime) {
        const a = timeToMinutes(startTime);
        const b = timeToMinutes(endTime);
        if (isNaN(a) || isNaN(b) || b <= a) return "";
        let diff = b - a;
        const h = Math.floor(diff / 60);
        const m = diff % 60;
        if (h && m) return `${h}h ${m}m`;
        if (h) return `${h}h`;
        return `${m}m`;
    }

    function sortForHome(items) {
        const open = items.filter((i) => !i.completed);
        const withDue = (d) => {
            if (!d) return Number.MAX_SAFE_INTEGER;
            const t = new Date(d + "T23:59:59").getTime();
            return isNaN(t) ? Number.MAX_SAFE_INTEGER : t;
        };
        return [...open].sort((a, b) => {
            const pa = PRIORITY_ORDER[a.priority] ?? 1;
            const pb = PRIORITY_ORDER[b.priority] ?? 1;
            if (pa !== pb) return pa - pb;
            return withDue(a.dueDate) - withDue(b.dueDate);
        });
    }

    function formatDueLabel(item) {
        if (!item.dueDate) return "No due date";
        const d = new Date(item.dueDate + "T12:00:00");
        const opts = { weekday: "short", month: "short", day: "numeric", year: "numeric" };
        let s = d.toLocaleDateString("en-US", opts);
        if (item.dueTime) s += " · " + item.dueTime;
        return s;
    }

    function typeLabel(t) {
        const m = { homework: "Homework", exam: "Exam", project: "Project", assignment: "Assignment", other: "Other" };
        return m[t] || "Other";
    }

    function priorityBadgeClass(p) {
        if (p === "HIGH") return "badge-priority-high";
        if (p === "LOW") return "badge-priority-low";
        return "badge-priority-medium";
    }

    /** Local calendar date at noon — avoids DST midnight shifting the weekday. */
    function atLocalNoon(d) {
        const x = d instanceof Date ? d : new Date(d);
        return new Date(x.getFullYear(), x.getMonth(), x.getDate(), 12, 0, 0, 0);
    }

    /** Monday 00:00 local of the week that contains d (week runs Mon–Sun). */
    function startOfWeekMonday(d) {
        const x = atLocalNoon(d);
        const day = x.getDay(); // 0 Sun … 6 Sat
        const daysSinceMonday = day === 0 ? 6 : day - 1;
        x.setDate(x.getDate() - daysSinceMonday);
        x.setHours(0, 0, 0, 0);
        return x;
    }

    function addDays(d, n) {
        const x = atLocalNoon(d);
        x.setDate(x.getDate() + n);
        x.setHours(0, 0, 0, 0);
        return x;
    }

    function toISODate(d) {
        const x = atLocalNoon(d);
        const y = x.getFullYear();
        const m = String(x.getMonth() + 1).padStart(2, "0");
        const day = String(x.getDate()).padStart(2, "0");
        return `${y}-${m}-${day}`;
    }

    function renderDeadlineAlerts() {
        const host = document.getElementById("deadline-alert-host");
        if (!host) return;
        host.innerHTML = "";
        const now = Date.now();
        const horizon = now + 48 * 60 * 60 * 1000;
        const items = getItems().filter((i) => !i.completed && i.dueDate);
        const urgent = items.filter((i) => {
            const t = new Date(i.dueDate + (i.dueTime ? "T" + i.dueTime : "T23:59:59")).getTime();
            return !isNaN(t) && t >= now && t <= horizon;
        });
        if (!urgent.length) return;
        const div = document.createElement("div");
        div.className = "alert alert-warning border-0 shadow-sm mb-0";
        div.setAttribute("role", "alert");
        div.innerHTML =
            `<strong><i class="fas fa-bell me-2"></i>Deadline reminders</strong> — ` +
            urgent.length +
            " item(s) due within 48 hours: " +
            urgent
                .map((u) => `<span class="fw-semibold">${escapeHtml(u.title)}</span>`)
                .join(", ");
        host.appendChild(div);
    }

    function escapeHtml(s) {
        const d = document.createElement("div");
        d.textContent = s;
        return d.innerHTML;
    }

    function escapeAttr(s) {
        return String(s)
            .replace(/&/g, "&amp;")
            .replace(/"/g, "&quot;")
            .replace(/</g, "&lt;");
    }

    function maybeNotify(items) {
        if (!("Notification" in window) || Notification.permission !== "granted") return;
        const now = Date.now();
        const horizon = now + 24 * 60 * 60 * 1000;
        items.forEach((i) => {
            if (i.completed || !i.dueDate) return;
            const t = new Date(i.dueDate + (i.dueTime ? "T" + i.dueTime : "T09:00:00")).getTime();
            if (isNaN(t) || t < now || t > horizon) return;
            const key = "studyplan_notified_" + i.id + "_" + toISODate(new Date(t));
            if (sessionStorage.getItem(key)) return;
            sessionStorage.setItem(key, "1");
            try {
                new Notification("StudyPlan: " + i.title, { body: "Due soon — check your list." });
            } catch (_) {}
        });
    }

    function initRemindersButton() {
        const btn = document.getElementById("btn-enable-reminders");
        if (!btn) return;
        btn.addEventListener("click", async () => {
            if (!("Notification" in window)) {
                alert("Notifications are not supported in this browser.");
                return;
            }
            const p = await Notification.requestPermission();
            if (p === "granted") {
                btn.classList.remove("btn-sp-blue");
                btn.classList.add("btn-success");
                btn.innerHTML = '<i class="fas fa-check me-1"></i>Reminders on';
                btn.disabled = true;
                maybeNotify(getItems());
            }
        });
    }

    function renderHome() {
        const listEl = document.getElementById("todo-list");
        const emptyEl = document.getElementById("todo-empty");
        const countEl = document.getElementById("todo-count");
        if (!listEl) return;

        const all = getItems();
        const sorted = sortForHome(all);
        const openCount = all.filter((i) => !i.completed).length;

        if (countEl) countEl.textContent = openCount + " open";

        listEl.querySelectorAll(".todo-item-row").forEach((n) => n.remove());
        if (emptyEl) emptyEl.style.display = sorted.length ? "none" : "";

        sorted.forEach((item) => {
            const li = document.createElement("li");
            li.className = "list-group-item todo-item-row" + (item.completed ? " completed" : "");
            li.dataset.id = item.id;
            li.innerHTML = `
                <div class="d-flex flex-column flex-md-row gap-2 align-items-start justify-content-between">
                    <div class="flex-grow-1 min-w-0">
                        <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                            <span class="badge bg-secondary">${escapeHtml(typeLabel(item.type))}</span>
                            <span class="badge ${priorityBadgeClass(item.priority)}">${escapeHtml(item.priority)}</span>
                            ${item.course ? `<span class="text-muted small">${escapeHtml(item.course)}</span>` : ""}
                        </div>
                        <div class="fw-semibold todo-title">${escapeHtml(item.title)}</div>
                        <div class="small text-muted">${escapeHtml(formatDueLabel(item))}</div>
                        ${item.notes ? `<div class="small mt-1">${escapeHtml(item.notes)}</div>` : ""}
                    </div>
                    <div class="d-flex flex-wrap gap-1 align-items-center">
                        <select class="form-select form-select-sm sp-priority-select" style="width:auto;min-width:7rem" data-id="${escapeHtml(item.id)}" aria-label="Priority">
                            <option value="HIGH" ${item.priority === "HIGH" ? "selected" : ""}>HIGH</option>
                            <option value="MEDIUM" ${item.priority === "MEDIUM" ? "selected" : ""}>MEDIUM</option>
                            <option value="LOW" ${item.priority === "LOW" ? "selected" : ""}>LOW</option>
                        </select>
                        <button type="button" class="btn btn-sm btn-outline-success sp-complete" data-id="${escapeHtml(item.id)}" title="Mark done">
                            <i class="fas fa-check"></i>
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-danger sp-delete" data-id="${escapeHtml(item.id)}" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>`;
            listEl.appendChild(li);
        });

        listEl.querySelectorAll(".sp-priority-select").forEach((sel) => {
            sel.addEventListener("change", () => {
                const id = sel.dataset.id;
                const items = getItems();
                const it = items.find((x) => x.id === id);
                if (it) {
                    it.priority = sel.value;
                    saveItems(items);
                    renderHome();
                }
            });
        });
        listEl.querySelectorAll(".sp-complete").forEach((btn) => {
            btn.addEventListener("click", () => {
                const id = btn.dataset.id;
                const items = getItems();
                const it = items.find((x) => x.id === id);
                if (it) {
                    it.completed = true;
                    saveItems(items);
                    renderHome();
                    renderDeadlineAlerts();
                }
            });
        });
        listEl.querySelectorAll(".sp-delete").forEach((btn) => {
            btn.addEventListener("click", () => {
                const id = btn.dataset.id;
                saveItems(getItems().filter((x) => x.id !== id));
                renderHome();
                renderDeadlineAlerts();
            });
        });
    }

    function initHomeForm() {
        const form = document.getElementById("form-add-item");
        if (!form) return;
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const title = document.getElementById("item-title")?.value?.trim();
            if (!title) return;
            const item = {
                id: uid(),
                title,
                type: document.getElementById("item-type")?.value || "homework",
                course: document.getElementById("item-course")?.value?.trim() || "",
                dueDate: document.getElementById("item-due")?.value || "",
                dueTime: document.getElementById("item-time")?.value || "",
                priority: document.getElementById("item-priority")?.value || "MEDIUM",
                notes: document.getElementById("item-notes")?.value?.trim() || "",
                completed: false,
                createdAt: new Date().toISOString(),
            };
            const items = getItems();
            items.push(item);
            saveItems(items);
            form.reset();
            document.getElementById("item-priority").value = "MEDIUM";
            renderHome();
            renderDeadlineAlerts();
            maybeNotify(getItems());
        });
    }

    let calWeekOffset = 0;
    let calSelectedIso = null;

    function blocksForDate(iso) {
        return getBlocks()
            .filter((b) => b.date === iso)
            .sort((a, b) => timeToMinutes(a.startTime) - timeToMinutes(b.startTime));
    }

    function refreshWorkBlockLinkedSelect() {
        const sel = document.getElementById("wb-linked");
        if (!sel) return;
        const prev = sel.value;
        sel.innerHTML = '<option value="">— none —</option>';
        getItems()
            .filter((i) => !i.completed)
            .forEach((i) => {
                const opt = document.createElement("option");
                opt.value = i.id;
                opt.textContent = (i.course ? i.course + ": " : "") + i.title;
                sel.appendChild(opt);
            });
        if (prev && [...sel.options].some((o) => o.value === prev)) sel.value = prev;
    }

    function initCalendarTabSync() {
        const tabsEl = document.getElementById("calendar-day-tabs");
        if (!tabsEl || tabsEl.dataset.wbSync) return;
        tabsEl.dataset.wbSync = "1";
        tabsEl.addEventListener("shown.bs.tab", (e) => {
            const target = e.target.getAttribute("data-bs-target") || "";
            const iso = target.replace("#cal-pane-", "");
            if (iso) {
                calSelectedIso = iso;
                const dateInp = document.getElementById("wb-date");
                if (dateInp) dateInp.value = iso;
            }
        });
    }

    function initWorkBlockForm() {
        const form = document.getElementById("form-work-block");
        if (!form) return;

        document.getElementById("wb-linked")?.addEventListener("change", () => {
            const id = document.getElementById("wb-linked")?.value;
            const titleInp = document.getElementById("wb-title");
            if (!id || !titleInp || titleInp.value.trim()) return;
            const it = getItems().find((x) => x.id === id);
            if (it) titleInp.value = it.title;
        });

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const date = document.getElementById("wb-date")?.value;
            const start = document.getElementById("wb-start")?.value;
            const durationRaw = document.getElementById("wb-duration")?.value;
            const endInput = document.getElementById("wb-end")?.value;
            const linkedId = document.getElementById("wb-linked")?.value || "";
            let title = document.getElementById("wb-title")?.value?.trim() || "";

            if (!date || !start) return;

            const startM = timeToMinutes(start);
            if (isNaN(startM)) return;

            let endM;
            const duration = durationRaw === "" || durationRaw == null ? NaN : parseFloat(durationRaw);
            if (!isNaN(duration) && duration > 0) {
                endM = startM + Math.round(duration * 60);
            } else if (endInput) {
                endM = timeToMinutes(endInput);
            } else {
                alert("Enter a duration in hours (e.g. 5) or an end time.");
                return;
            }

            if (isNaN(endM) || endM <= startM) {
                alert("End time must be after start time.");
                return;
            }
            if (endM >= 24 * 60) {
                alert("This block must end before midnight. Split overnight work into two days.");
                return;
            }

            const endTime = minutesToTime(endM);
            if (linkedId && !title) {
                const it = getItems().find((x) => x.id === linkedId);
                if (it) title = it.title;
            }
            if (!title) {
                alert("Add a short label or link a to-do item.");
                return;
            }

            const block = {
                id: uid(),
                date,
                startTime: start,
                endTime,
                title,
                linkedItemId: linkedId || undefined,
                createdAt: new Date().toISOString(),
            };
            const blocks = getBlocks();
            blocks.push(block);
            saveBlocks(blocks);
            document.getElementById("wb-duration").value = "";
            document.getElementById("wb-end").value = "";
        });
    }

    function renderCalendar() {
        const tabs = document.getElementById("calendar-day-tabs");
        const panels = document.getElementById("calendar-tab-panels");
        if (!tabs || !panels) return;

        const base = addDays(startOfWeekMonday(new Date()), calWeekOffset * 7);
        const days = [];
        for (let i = 0; i < 7; i++) days.push(addDays(base, i));

        const weekIsos = days.map((d) => toISODate(d));
        const activeIso =
            calSelectedIso && weekIsos.includes(calSelectedIso) ? calSelectedIso : weekIsos[0];

        tabs.innerHTML = "";
        panels.innerHTML = "";
        const items = getItems();

        days.forEach((d) => {
            const iso = toISODate(d);
            const label = d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
            const isToday = toISODate(new Date()) === iso;
            const tabId = "cal-tab-" + iso;
            const paneId = "cal-pane-" + iso;
            const isActiveTab = iso === activeIso;

            const li = document.createElement("li");
            li.className = "nav-item";
            const a = document.createElement("button");
            a.type = "button";
            a.className = "nav-link" + (isActiveTab ? " active" : "") + (isToday ? " fw-bold" : "");
            a.id = tabId;
            a.dataset.bsToggle = "tab";
            a.dataset.bsTarget = "#" + paneId;
            a.role = "tab";
            a.setAttribute("aria-controls", paneId);
            a.setAttribute("aria-selected", isActiveTab ? "true" : "false");
            a.textContent = isToday ? label + " (today)" : label;
            li.appendChild(a);
            tabs.appendChild(li);

            const dayItems = items.filter((it) => it.dueDate === iso && !it.completed);
            const dayBlocks = blocksForDate(iso);
            const pane = document.createElement("div");
            pane.className = "tab-pane fade cal-day-panel" + (isActiveTab ? " show active" : "");
            pane.id = paneId;
            pane.role = "tabpanel";
            pane.setAttribute("aria-labelledby", tabId);

            const wrap = document.createElement("div");
            wrap.className = "d-flex flex-column gap-4";

            const deadlinesSection = document.createElement("div");
            deadlinesSection.innerHTML = '<div class="cal-section-title text-sp-green"><i class="fas fa-flag-checkered me-1"></i>Deadlines</div>';
            if (!dayItems.length) {
                const empty = document.createElement("div");
                empty.className = "card border-0 shadow-sm";
                empty.innerHTML =
                    '<div class="card-body text-muted small">Nothing due this day. Add tasks with a due date on the To-Do page.</div>';
                deadlinesSection.appendChild(empty);
            } else {
                const ul = document.createElement("ul");
                ul.className = "list-group shadow-sm";
                dayItems.forEach((it) => {
                    const row = document.createElement("li");
                    row.className = "list-group-item cal-due-item";
                    row.innerHTML = `
                        <div class="d-flex justify-content-between gap-2 flex-wrap">
                            <div>
                                <span class="badge ${priorityBadgeClass(it.priority)} me-1">${escapeHtml(it.priority)}</span>
                                <span class="badge bg-secondary">${escapeHtml(typeLabel(it.type))}</span>
                                <div class="fw-semibold mt-1">${escapeHtml(it.title)}</div>
                                ${it.course ? `<div class="small text-muted">${escapeHtml(it.course)}</div>` : ""}
                                ${it.dueTime ? `<div class="small text-muted">Due time: ${escapeHtml(it.dueTime)}</div>` : ""}
                            </div>
                        </div>`;
                    ul.appendChild(row);
                });
                deadlinesSection.appendChild(ul);
            }
            wrap.appendChild(deadlinesSection);

            const blocksSection = document.createElement("div");
            blocksSection.innerHTML =
                '<div class="cal-section-title text-sp-blue"><i class="fas fa-user-clock me-1"></i>Reserved work time</div>';
            if (!dayBlocks.length) {
                const emptyB = document.createElement("div");
                emptyB.className = "card border-0 shadow-sm";
                emptyB.innerHTML =
                    '<div class="card-body text-muted small">No blocks yet. Use the form above to reserve time (try duration <strong>5</strong> hours for a long assignment).</div>';
                blocksSection.appendChild(emptyB);
            } else {
                const ulb = document.createElement("ul");
                ulb.className = "list-group shadow-sm";
                dayBlocks.forEach((wb) => {
                    const linked = wb.linkedItemId ? getItems().find((x) => x.id === wb.linkedItemId) : null;
                    const dur = formatBlockDuration(wb.startTime, wb.endTime);
                    const row = document.createElement("li");
                    row.className = "list-group-item work-block-item";
                    row.innerHTML = `
                        <div class="d-flex justify-content-between gap-2 flex-wrap align-items-start">
                            <div>
                                <span class="badge bg-sp-blue me-1">${escapeHtml(wb.startTime)} – ${escapeHtml(wb.endTime)}</span>
                                ${dur ? `<span class="badge bg-light text-dark border">${escapeHtml(dur)}</span>` : ""}
                                <div class="fw-semibold mt-2">${escapeHtml(wb.title)}</div>
                                ${
                                    linked
                                        ? `<div class="small text-muted"><i class="fas fa-link me-1"></i>Linked: ${escapeHtml(linked.title)}</div>`
                                        : ""
                                }
                            </div>
                            <button type="button" class="btn btn-sm btn-outline-danger wb-delete" data-id="${escapeAttr(wb.id)}" title="Remove block">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>`;
                    ulb.appendChild(row);
                });
                blocksSection.appendChild(ulb);
            }
            wrap.appendChild(blocksSection);

            pane.appendChild(wrap);
            panels.appendChild(pane);
        });

        calSelectedIso = activeIso;
        const dateInp = document.getElementById("wb-date");
        if (dateInp) dateInp.value = activeIso;
        refreshWorkBlockLinkedSelect();

        panels.querySelectorAll(".wb-delete").forEach((btn) => {
            btn.addEventListener("click", () => {
                const id = btn.dataset.id;
                saveBlocks(getBlocks().filter((b) => b.id !== id));
            });
        });
    }

    function initCalendarNav() {
        document.getElementById("cal-prev-week")?.addEventListener("click", () => {
            calWeekOffset--;
            renderCalendar();
        });
        document.getElementById("cal-this-week")?.addEventListener("click", () => {
            calWeekOffset = 0;
            renderCalendar();
        });
        document.getElementById("cal-next-week")?.addEventListener("click", () => {
            calWeekOffset++;
            renderCalendar();
        });
    }

    function getGradeRows() {
        try {
            const raw = localStorage.getItem(STORAGE_GRADES);
            if (raw) {
                const data = JSON.parse(raw);
                if (data && Array.isArray(data.rows) && data.rows.length) return data.rows;
            }
        } catch (_) {}
        return [
            { name: "Homework", weight: 30, score: "" },
            { name: "Midterm", weight: 30, score: "" },
            { name: "Final", weight: 40, score: "" },
        ];
    }

    function saveGradeRows(rows) {
        localStorage.setItem(STORAGE_GRADES, JSON.stringify({ rows }));
    }

    function renderGrades() {
        const tbody = document.getElementById("grade-tbody");
        const hint = document.getElementById("grade-weight-hint");
        const result = document.getElementById("grade-result");
        const detail = document.getElementById("grade-result-detail");
        if (!tbody) return;

        const rows = getGradeRows();
        tbody.innerHTML = "";
        rows.forEach((row, idx) => {
            const tr = document.createElement("tr");
            const wVal = row.weight === "" || row.weight == null ? "" : String(row.weight);
            const sVal = row.score === "" || row.score == null ? "" : String(row.score);
            tr.innerHTML = `
                <td><input type="text" class="form-control form-control-sm grade-name" data-idx="${idx}" value="${escapeAttr(row.name)}"></td>
                <td><input type="number" class="form-control form-control-sm grade-weight" data-idx="${idx}" min="0" max="100" step="0.1" value="${escapeAttr(wVal)}"></td>
                <td><input type="number" class="form-control form-control-sm grade-score" data-idx="${idx}" min="0" max="100" step="0.1" placeholder="%" value="${escapeAttr(sVal)}"></td>
                <td><button type="button" class="btn btn-sm btn-outline-danger grade-remove" data-idx="${idx}"><i class="fas fa-times"></i></button></td>`;
            tbody.appendChild(tr);
        });

        function recalc() {
            const names = [...tbody.querySelectorAll(".grade-name")];
            const newRows = names.map((inp, i) => {
                const w = tbody.querySelector(`.grade-weight[data-idx="${i}"]`);
                const s = tbody.querySelector(`.grade-score[data-idx="${i}"]`);
                return {
                    name: inp.value || "Category",
                    weight: w.value === "" ? "" : parseFloat(w.value),
                    score: s.value === "" ? "" : parseFloat(s.value),
                };
            });
            saveGradeRows(newRows);

            let sumW = 0;
            newRows.forEach((r) => {
                if (typeof r.weight === "number" && !isNaN(r.weight)) sumW += r.weight;
            });
            if (hint) {
                hint.textContent =
                    Math.abs(sumW - 100) < 0.01
                        ? "Weights total 100%."
                        : `Weights total ${sumW.toFixed(1)}%. For a true course average, aim for 100%.`;
            }

            let num = 0;
            let den = 0;
            newRows.forEach((r) => {
                if (typeof r.weight === "number" && typeof r.score === "number" && !isNaN(r.weight) && !isNaN(r.score)) {
                    num += (r.weight / 100) * r.score;
                    den += r.weight;
                }
            });
            if (result) {
                if (den <= 0 || newRows.every((r) => r.score === "")) {
                    result.textContent = "—";
                    if (detail) detail.textContent = "Enter scores to see your weighted average.";
                } else {
                    const course = den > 0 ? (num / (den / 100)).toFixed(2) : "—";
                    result.textContent = course + "%";
                    if (detail) detail.textContent = `Based on ${den.toFixed(1)}% of entered weights with scores.`;
                }
            }
        }

        tbody.querySelectorAll("input").forEach((inp) => inp.addEventListener("input", recalc));
        tbody.querySelectorAll(".grade-remove").forEach((btn) => {
            btn.addEventListener("click", () => {
                const i = parseInt(btn.dataset.idx, 10);
                const r = getGradeRows();
                r.splice(i, 1);
                if (!r.length) r.push({ name: "Category", weight: 100, score: "" });
                saveGradeRows(r);
                renderGrades();
            });
        });
        recalc();
    }

    function initGradeAdd() {
        document.getElementById("grade-add-row")?.addEventListener("click", () => {
            const r = getGradeRows();
            r.push({ name: "New category", weight: 0, score: "" });
            saveGradeRows(r);
            renderGrades();
        });
    }

    let charts = { completion: null, types: null, priority: null };

    function destroyChart(c) {
        if (c) {
            c.destroy();
        }
        return null;
    }

    function renderProgress() {
        if (typeof Chart === "undefined") return;

        const items = getItems();
        const open = items.filter((i) => !i.completed);
        const done = items.filter((i) => i.completed);

        const compEl = document.getElementById("chart-completion");
        const typesEl = document.getElementById("chart-types");
        const priEl = document.getElementById("chart-priority");
        const summary = document.getElementById("progress-summary");

        const cardinal = getComputedStyle(document.documentElement).getPropertyValue("--sp-cardinal").trim() || "#c41e3a";
        const blue = getComputedStyle(document.documentElement).getPropertyValue("--sp-blue").trim() || "#1e5f8c";
        const green = getComputedStyle(document.documentElement).getPropertyValue("--sp-green").trim() || "#1f7a4a";

        if (compEl) {
            charts.completion = destroyChart(charts.completion);
            charts.completion = new Chart(compEl, {
                type: "doughnut",
                data: {
                    labels: ["Open", "Completed"],
                    datasets: [{ data: [open.length, done.length], backgroundColor: [blue, green], borderWidth: 0 }],
                },
                options: { plugins: { legend: { position: "bottom" } }, maintainAspectRatio: false },
            });
        }

        const typeKeys = ["homework", "exam", "project", "assignment", "other"];
        const typeCounts = {};
        typeKeys.forEach((k) => (typeCounts[k] = 0));
        open.forEach((i) => {
            const k = typeKeys.includes(i.type) ? i.type : "other";
            typeCounts[k]++;
        });
        if (typesEl) {
            charts.types = destroyChart(charts.types);
            charts.types = new Chart(typesEl, {
                type: "bar",
                data: {
                    labels: typeKeys.map((k) => typeLabel(k)),
                    datasets: [{ label: "Open tasks", data: typeKeys.map((k) => typeCounts[k]), backgroundColor: green }],
                },
                options: {
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
                    maintainAspectRatio: false,
                },
            });
        }

        let h = 0,
            m = 0,
            l = 0;
        open.forEach((i) => {
            if (i.priority === "HIGH") h++;
            else if (i.priority === "LOW") l++;
            else m++;
        });
        if (priEl) {
            charts.priority = destroyChart(charts.priority);
            charts.priority = new Chart(priEl, {
                type: "pie",
                data: {
                    labels: ["HIGH", "MEDIUM", "LOW"],
                    datasets: [{ data: [h, m, l], backgroundColor: [cardinal, blue, green], borderWidth: 0 }],
                },
                options: { plugins: { legend: { position: "bottom" } }, maintainAspectRatio: false },
            });
        }

        if (summary) {
            summary.innerHTML = `
                <li class="col-md-4 mb-2"><strong>${items.length}</strong> total tasks</li>
                <li class="col-md-4 mb-2"><strong>${open.length}</strong> open</li>
                <li class="col-md-4 mb-2"><strong>${done.length}</strong> completed</li>`;
        }
    }

    function bodyPage() {
        const b = document.body;
        if (!b || !b.className) return "";
        const m = b.className.match(/page-(\w+)/);
        return m ? m[1] : "";
    }

    function init() {
        renderDeadlineAlerts();
        initRemindersButton();

        const page = bodyPage();
        if (page === "home") {
            initHomeForm();
            renderHome();
        }
        if (page === "calendar") {
            initCalendarTabSync();
            initWorkBlockForm();
            initCalendarNav();
            renderCalendar();
        }
        if (page === "grades") {
            initGradeAdd();
            renderGrades();
        }
        if (page === "progress") {
            if (document.fonts && document.fonts.ready) {
                document.fonts.ready.then(() => renderProgress());
            } else {
                renderProgress();
            }
        }

        window.addEventListener("studyplan:itemschanged", () => {
            renderDeadlineAlerts();
            if (page === "home") renderHome();
            if (page === "calendar") {
                refreshWorkBlockLinkedSelect();
                renderCalendar();
            }
            if (page === "progress") renderProgress();
            maybeNotify(getItems());
        });

        window.addEventListener("studyplan:blockschanged", () => {
            if (page === "calendar") renderCalendar();
        });

        setInterval(() => {
            maybeNotify(getItems());
            if (page === "home" || !page) renderDeadlineAlerts();
        }, 60 * 1000);
    }

    document.addEventListener("DOMContentLoaded", init);
})();
