 var awardPage = 2;
 var awardPageSize = 10;
 var awardProcessing;
 var awardScrollPos = 0;
$(document).ready(function(){

});
function loadMoreAwards(award_type){
     $.ajax({
         url: app_base_url+'awards/load-more-awards',
         type: 'post',
         dataType: 'json',
         cache: false,
         data: {'page': awardPage, 'page_size': awardPageSize, 'award_type': award_type},
         beforeSend: function(){
             //$('.overlay').show();
             if(award_type == 'given'){
                $('#loadMoreAwardsGiven').text('Loading Please Wait...');
                $('#loadMoreAwardsGiven').prop('disabled',true);
             }else{
                $('#loadMoreAwardsReceived').text('Loading Please Wait...');
                $('#loadMoreAwardsReceived').prop('disabled',true);
             }

         },
         success: function(response){
             //$('.overlay').hide();
             $('#loadMoreAwards').prop('disabled',false);
             $('#loadMoreAwards').removeProp('disabled');
             $('#loadMoreAwards').text('Load More');
             if(response.award_type == 'given'){
                $('#loadMoreAwardsGiven').prop('disabled',false);
                 $('#loadMoreAwardsGiven').removeProp('disabled');
                 $('#loadMoreAwardsGiven').text('Load More');
             }else{
                $('#loadMoreAwardsReceived').prop('disabled',false);
                 $('#loadMoreAwardsReceived').removeProp('disabled');
                 $('#loadMoreAwardsReceived').text('Load More');
             }
             if(response.error == 0){

                //$('#activitySection').append();
                 /*$("#chat_listings").append(response.chat_listing_html);
                 if(response.last_master_id){
                     $('#last_master_id').val(response.last_master_id);
                 }*/
                 if(response.award_type == 'given'){
                     if(response.award_data != ""){
                        $('#awardGivenData').append(response.award_data);
                        awardPage = awardPage+1;
                        $('#loadMoreAwardGiven').show();
                     }else{
                        $('#loadMoreAwardGiven').hide();
                     }
                 }else{
                    if(response.award_data != ""){
                        $('#awardReceivedData').append(response.award_data);
                        awardPage = awardPage+1;
                        $('#loadMoreAwardReceived').show();
                     }else{
                        $('#loadMoreAwardReceived').hide();
                     }
                 }
                // activityProcessing = false;

             }
         }
     });
 }