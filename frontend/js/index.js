(function () {

    const boot = async ()=>{
        await authenticaotr.configureClient();

        document.getElementById('btn-login')
        .addEventListener('click', authenticaotr.login);
    }
    
    boot()
})()