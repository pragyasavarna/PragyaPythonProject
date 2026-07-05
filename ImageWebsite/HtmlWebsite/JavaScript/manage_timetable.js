document.addEventListener("DOMContentLoaded", function () {
    // ==========================================
    // 1. SECTION SWITCHER LOGIC
    // ==========================================
    const sectionSelector = document.getElementById("section-selector");
    const sections = document.querySelectorAll(".manage-section");

    function showSection(sectionId) {
        // Hide all sections
        sections.forEach(sec => sec.classList.add("hidden"));

        // Show the selected section
        const activeSection = document.getElementById(sectionId);
        if (activeSection) {
            activeSection.classList.remove("hidden");
        }

        // Save choice to localStorage so page reloads don't reset the view
        localStorage.setItem("activeManageSection", sectionId);
    }

    if (sectionSelector) {
        // Restore previous section or default to 'entries'
        const savedSection = localStorage.getItem("activeManageSection") || "section-entries";
        sectionSelector.value = savedSection;
        showSection(savedSection);

        // Listen for user changes
        sectionSelector.addEventListener("change", (e) => {
            showSection(e.target.value);
            const messageBox = document.querySelector('.message-container');
            if (messageBox) {
                messageBox.style.display = 'none';
            }
        });
    }

    // ==========================================
    // 2. DYNAMIC SUBJECT FILTER LOGIC
    // ==========================================
    const teacherSelect = document.getElementById("frontend-teacher-select");
    const subjectSelect = document.getElementById("frontend-subject-select");

    const teacherDataElement = document.getElementById("teacher-data");
    let teacherSubjectsMap = {};

    if (teacherDataElement) {
        try {
            // Read the initial data
            let rawData = JSON.parse(teacherDataElement.textContent);

            // BULLETPROOF FIX: If Django double-encoded it as a string, parse it again
            if (typeof rawData === 'string') {
                rawData = JSON.parse(rawData);
            }

            teacherSubjectsMap = rawData;
        } catch (e) {
            console.error("Error parsing teacher subject data:", e);
        }
    }

    function updateSubjects() {
        const teacherId = teacherSelect.value;
        subjectSelect.innerHTML = '<option value="">---------</option>';

        if (teacherId && teacherSubjectsMap[teacherId]) {
            const subjects = teacherSubjectsMap[teacherId];

            // Ensure subjects is actually an array before trying to run .forEach
            if (Array.isArray(subjects)) {
                subjects.forEach(subject => {
                    const option = document.createElement("option");
                    option.value = subject.id;
                    option.textContent = subject.name;
                    subjectSelect.appendChild(option);
                });
            } else {
                console.warn("Subjects data is not an array for teacher ID:", teacherId);
            }
        } else {
            subjectSelect.innerHTML = '<option value="">Select Teacher First</option>';
        }
    }

    if (teacherSelect && subjectSelect) {
        teacherSelect.addEventListener("change", updateSubjects);
        updateSubjects();
    }

    // ==========================================
    // 3. CLASS TIMETABLE FILTER LOGIC
    // ==========================================
    const classSelect = document.getElementById("frontend-class-select");
    const classWrappers = document.querySelectorAll(".class-timetable-wrapper");
    const noClassMsg = document.getElementById("no-class-selected-msg");

    function updateVisibleTimetable() {
        if (!classSelect || !classWrappers) return;

        const selectedClassId = classSelect.value;

        // Hide or show the matching table
        classWrappers.forEach(wrapper => {
            if (wrapper.getAttribute("data-class-id") === selectedClassId) {
                wrapper.classList.remove("hidden");
            } else {
                wrapper.classList.add("hidden");
            }
        });

        // Hide or show the "Please select a class" message
        if (noClassMsg) {
            if (selectedClassId) {
                noClassMsg.classList.add("hidden");
                // Save selection so it persists after page reload (e.g. after adding an entry)
                localStorage.setItem("activeTimetableClass", selectedClassId);
            } else {
                noClassMsg.classList.remove("hidden");
                localStorage.removeItem("activeTimetableClass");
            }
        }
    }

    if (classSelect) {
        // Restore class selection from local storage if available
        const savedClass = localStorage.getItem("activeTimetableClass");
        if (savedClass) {
            // Ensure the saved class actually exists in the current dropdown before setting
            const optionExists = Array.from(classSelect.options).some(opt => opt.value === savedClass);
            if (optionExists) {
                classSelect.value = savedClass;
            }
        }

        // Listen for changes
        classSelect.addEventListener("change", updateVisibleTimetable);

        // Trigger immediately on page load
        updateVisibleTimetable();
    }
});