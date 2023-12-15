// prepare statistic data table
const StatisticTable = Component.StatisticTable.DataTable({
    ajax: {
        method: "GET",
        url: Constants.StatisticUrl
    },
    columns: [
        {data: "name"},
        {data: "p"},
        {data: "w"},
        {data: "d"},
        {data: "l"},
        {data: "pts"},
    ],
    processing: true,
});

// prepare final rank data table
const rankTable = Component.RankTable.DataTable({
    ajax: {
        method: "GET",
        url: Constants.RankUrl
    },
    columns: [
        {data: "rank"},
        {data: "team"},
        {data: "point"},
    ],
    ordering: false,
    processing: true,
});

// prepare league data table
const LeagueTable = Component.LeagueTable.DataTable({
    ajax: {
        method: "GET",
        url: Constants.LeagueUrl,
    },
    columns: [
        {data: "home"},
        {data: "home_score"},
        {data: "away"},
        {data: "away_score"},
        {
            data: "id",
            render: function (data, type, row, meta) {
                const editBtn = `<button class="btn xs btn-warning" data-model-name="edit">Edit</button>`
                const deleteBtn = `<button class="btn xs btn-danger" data-model-name="delete">Delete</button>`
                return `${editBtn} | ${deleteBtn}`;
            },
        },
    ],
    processing: true,
});

// prepare teams data table
const TeamsTable = Component.TeamTable.DataTable({
    ajax: {
        method: "GET",
        url: Constants.TeamUrl
    },
    columns: [
        {data: "name"},
        {
            data: "id",
            render: function (data, type, row, meta) {
                const editBtn = `<button class="btn xs btn-warning" data-model-name="edit">Edit</button>`
                const deleteBtn = `<button class="btn xs btn-danger" data-model-name="delete">Delete</button>`
                return `${editBtn} | ${deleteBtn}`;
            },
        },
    ],
    processing: true,
});
