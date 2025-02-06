// Ejecutar cuando la pagina este lista
document.addEventListener("DOMContentLoaded", async () => {
	const modalToggles = document.querySelectorAll("[data-modal-toggle]");
	const dialogs = document.querySelectorAll("dialog");

	function toggleModal(dialog) {
		if (dialog.open) dialog.close();
		else dialog.showModal();
	}

	modalToggles.forEach((toggle) => {
		const modal = document.getElementById(toggle.dataset.modalToggle);

		if (!modal) return;

		toggle.addEventListener("click", () => toggleModal(modal));
	});
	dialogs.forEach((dialog) => {
		dialog.addEventListener("click", (event) => {
			if (event.target !== dialog) return;

			toggleModal(dialog);
		});
	});
});
