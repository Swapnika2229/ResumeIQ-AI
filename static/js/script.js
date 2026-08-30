// =====================================================
// ResumeIQ AI - Main JavaScript
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    // =================================================
    // RESUME OVERVIEW CHART
    // =================================================

    const resumeChart = document.getElementById("resumeChart");

    if (resumeChart && typeof Chart !== "undefined") {

        // Get dashboard values safely
        const ats = typeof atsScore !== "undefined"
            ? Number(atsScore) || 0
            : 0;

        const skills = typeof skillsCount !== "undefined"
            ? Number(skillsCount) || 0
            : 0;

        const jobs = typeof jobMatches !== "undefined"
            ? Number(jobMatches) || 0
            : 0;

        new Chart(resumeChart, {

            type: "doughnut",

            data: {

                labels: [
                    "ATS Score",
                    "Skills Found",
                    "Job Matches"
                ],

                datasets: [{
                    data: [
                        ats,
                        skills,
                        jobs
                    ],

                    borderWidth: 2
                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {
                            color: "white",
                            padding: 20,
                            font: {
                                size: 13
                            }
                        }

                    }

                }

            }

        });

    }


    // =================================================
    // CAREER PROGRESS CHART
    // =================================================

    const careerChart = document.getElementById("careerChart");

    if (careerChart && typeof Chart !== "undefined") {

        new Chart(careerChart, {

            type: "bar",

            data: {

                labels: [
                    "Resume",
                    "Interview",
                    "Projects",
                    "Skills"
                ],

                datasets: [{

                    label: "Progress",

                    data: [
                        85,
                        70,
                        90,
                        80
                    ],

                    borderWidth: 1

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        labels: {
                            color: "white"
                        }

                    }

                },

                scales: {

                    x: {

                        ticks: {
                            color: "white"
                        },

                        grid: {
                            color: "rgba(255,255,255,0.08)"
                        }

                    },

                    y: {

                        beginAtZero: true,

                        max: 100,

                        ticks: {
                            color: "white"
                        },

                        grid: {
                            color: "rgba(255,255,255,0.08)"
                        }

                    }

                }

            }

        });

    }


    // =================================================
    // LIVE CLOCK
    // =================================================

    function updateClock() {

        const clock = document.getElementById("liveTime");

        if (clock) {

            const now = new Date();

            clock.innerHTML = now.toLocaleString();

        }

    }

    // Start clock only if the element exists
    if (document.getElementById("liveTime")) {

        updateClock();

        setInterval(updateClock, 1000);

    }


    // =================================================
    // DARK / LIGHT THEME
    // =================================================

    const themeBtn = document.getElementById("themeToggle");

    if (themeBtn) {

        const savedTheme = localStorage.getItem("theme");

        if (savedTheme === "light") {

            document.body.classList.add("light-mode");

            themeBtn.innerHTML = "☀️";

        } else {

            themeBtn.innerHTML = "🌙";

        }


        themeBtn.onclick = function () {

            document.body.classList.toggle("light-mode");

            if (document.body.classList.contains("light-mode")) {

                localStorage.setItem("theme", "light");

                themeBtn.innerHTML = "☀️";

            } else {

                localStorage.setItem("theme", "dark");

                themeBtn.innerHTML = "🌙";

            }

        };

    }


    // =================================================
    // LOADING BOX
    // =================================================

    window.showLoading = function () {

        const box = document.getElementById("loadingBox");

        if (box) {

            box.style.display = "block";

        }

    };

});