/* StudyPlan.com — lightweight UI helpers */
document.addEventListener("DOMContentLoaded", () => {
    const collapse = document.querySelector(".navbar-collapse");
    if (collapse) {
        collapse.querySelectorAll(".nav-link").forEach((link) => {
            link.addEventListener("click", () => {
                if (window.innerWidth < 992 && typeof bootstrap !== "undefined") {
                    const inst = bootstrap.Collapse.getInstance(collapse);
                    if (inst) inst.hide();
                }
            });
        });
    }
});
