function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    var main = document.querySelector('.main');
    var body = document.body;

    if (sidebar.style.width === "0px" || sidebar.style.width === "") {
        sidebar.style.width = "250px"; /* Abre a sidebar */
        main.style.marginLeft = "250px"; /* Ajusta o conteúdo principal */
        body.classList.add('sidebar-open'); /* Adiciona a classe ao corpo */
    } else {
        sidebar.style.width = "0"; /* Fecha a sidebar */
        main.style.marginLeft = "0"; /* Ajusta o conteúdo principal */
        body.classList.remove('sidebar-open'); /* Remove a classe do corpo */
    }
}
