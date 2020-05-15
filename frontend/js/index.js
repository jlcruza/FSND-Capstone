(function () {

    const updateUI = async () => {
        await authenticaotr.configureClient()
        const isAuthenticated = await authenticaotr.auth0.isAuthenticated();

        console.log("isAuthenticated", isAuthenticated);
    };

    updateUI()
})()