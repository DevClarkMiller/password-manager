const blankNulls = (items) =>{
    for (let item of items){
        if(!item){
            item = ""
        }
    }
    return blankNulls;
}

module.exports = {blankNulls};