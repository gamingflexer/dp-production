
let searchFun=() =>{
    
    let filter = document.getElementById('searchbox').value.toUpperCase();
    
    let myTable = document.getElementById('table_data');
    
    let tr = myTable.getElementsByTagName('tr');
    

    for(let i=1;i<tr.length; i++){
        
        let td1=tr[i].getElementsByTagName('td')[1];
        let td2=tr[i].getElementsByTagName('td')[2];
        let td3=tr[i].getElementsByTagName('td')[3];
        let td4=tr[i].getElementsByTagName('td')[4];
        let td5=tr[i].getElementsByTagName('td')[5];
        let td6=tr[i].getElementsByTagName('td')[6];

        if(td1||td2 ||td3 ||td4||td5||td6){

            let textvalue1 = td1.textContent || td1.innerHTML;
            let textvalue2 = td2.textContent || td2.innerHTML;
            let textvalue3 = td3.textContent || td3.innerHTML;
            let textvalue4 = td4.textContent || td4.innerHTML;
            let textvalue5 = td5.textContent || td5.innerHTML;
            let textvalue6 = td6.textContent || td6.innerHTML;
            
            
            if(textvalue1.toUpperCase().indexOf(filter)>-1 || textvalue2.toUpperCase().indexOf(filter)>-1|| textvalue3.toUpperCase().indexOf(filter)>-1 || textvalue4.toUpperCase().indexOf(filter)>-1 || textvalue5.toUpperCase().indexOf(filter)>-1 || textvalue6.toUpperCase().indexOf(filter)>-1){
                
                tr[i].style.display="";
            }
            else{
                tr[i].style.display="none";
            }
        }
    }

}
