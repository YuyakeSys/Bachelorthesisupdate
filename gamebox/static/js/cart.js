var updateBtns = document.getElementsByClassName('update-cart')
var selectBtns = document.getElementsByClassName('select-game')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function (){
        var gameId = this.dataset.game
        var action = this.dataset.action
        console.log('gameId:',gameId, 'Action:', action);
        updateUserOrder(gameId, action)
    })
}


function updateUserOrder(gameId, action){
    console.log('Logged')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'gameId': gameId, 'action':action})

    })

        .then((response)=>{
            return response.json()
    })

        .then((data)=>{
            console.log('data', data)
            location.reload()
    })
}


for (i = 0; i < selectBtns.length; i++) {
    selectBtns[i].addEventListener('click', function (){
        var type = this.dataset.type
        var action = this.dataset.action
        console.log('type:',type, 'Action:', action);
        // updateUserOrder(gameId, action)
    })
}


function selectGames(type, action){
    console.log('selecting')

    var url = '/selectGame/?='+

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'gameId': gameId, 'action':action})

    })

        .then((response)=>{
            return response.json()
    })

        .then((data)=>{
            console.log('data', data)
            location.reload()
    })
}