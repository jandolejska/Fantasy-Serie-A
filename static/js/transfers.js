document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("playerSearch");
    const teamFilter = document.getElementById("teamFilter");
    const sortSelect = document.getElementById("sortPlayers");
    const playerCount = document.getElementById("playerCount");

    const players = Array.from(
        document.querySelectorAll(".transfer-player")
    );

    if (!players.length) {
        return;
    }

    // -------------------------
    // Naplnění klubů
    // -------------------------

    const teams = [...new Set(
        players.map(
            p => p.dataset.team
        )
    )].sort();

    teams.forEach(team => {

        const option = document.createElement("option");

        option.value = team;

        option.textContent =
            team.charAt(0).toUpperCase() +
            team.slice(1);

        teamFilter.appendChild(option);

    });

    // -------------------------
    // Filtrování
    // -------------------------

    function filterPlayers() {

        const search =
            searchInput.value.toLowerCase().trim();

        const selectedTeam =
            teamFilter.value;

        let visible = 0;

        players.forEach(player => {

            const name =
                player.dataset.name;

            const team =
                player.dataset.team;

            const matchSearch =
                name.includes(search) ||
                team.includes(search);

            const matchTeam =
                selectedTeam === "" ||
                team === selectedTeam;

            if (matchSearch && matchTeam) {

                player.classList.remove("d-none");

                visible++;

            }
            else {

                player.classList.add("d-none");

            }

        });

        let text = "hráčů";

        if (visible === 1) {
            text = "hráč";
        }
        else if (visible >= 2 && visible <= 4) {
            text = "hráči";
        }

        playerCount.textContent = `Nalezeno: ${visible} ${text}`;

    }

    // -------------------------
    // Řazení
    // -------------------------

    function sortPlayers() {

        const container =
            players[0].parentElement;

        players.sort((a, b) => {

            switch (sortSelect.value) {

                case "team":

                    return a.dataset.team.localeCompare(
                        b.dataset.team,
                        "cs"
                    );

                case "priceAsc":

                    return Number(a.dataset.price) -
                        Number(b.dataset.price);

                case "priceDesc":

                    return Number(b.dataset.price) -
                        Number(a.dataset.price);

                default:

                    return a.dataset.name.localeCompare(
                        b.dataset.name,
                        "cs"
                    );

            }

        });

        players.forEach(player => {

            container.appendChild(player);

        });

    }

    // -------------------------
    // Události
    // -------------------------

    searchInput.addEventListener(
        "input",
        filterPlayers
    );

    teamFilter.addEventListener(
        "change",
        filterPlayers
    );

    sortSelect.addEventListener(
        "change",
        () => {

            sortPlayers();

            filterPlayers();

        }
    );

    sortPlayers();

    filterPlayers();

});