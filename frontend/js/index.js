(function () {

    await authenticaotr.configureClient();

    document.getElementById('btn-login')
    .addEventListener('click', authenticaotr.login());
    
})()