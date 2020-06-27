function searchByTag(ddlId)
{
    let url = '/tags/' + $('#'+ddlId).val() + '/posts';
    window.location=url;
}

function toggleElement(source, id)
{
    let isInvalid = $(source).val() == '';

    $("#" + id).attr("disabled", isInvalid);

    if(isInvalid)
        $("#" + id).removeClass('btn-outline-info');
    else
        $("#" + id).addClass('btn-outline-info');
}

function show_me(elementId)
{
  $('#' + elementId).show();
}

function hide_me(elementId)
{
  $('#' + elementId).hide();
}

function subscribeMe(postId, csrfToken)
{
    url = "/post/" + postId +"/subscribe";
    //console.info('subscriptionUrl', subscriptionUrl);
    $.ajax({
        url: url,
        type: "POST",
        data: {  csrfmiddlewaretoken: csrfToken, //django needs this
                 data_item: {'post_id':postId}},
        timeout:0,
        success: function(data){
            if(data.result == true) {
                $('#subscribe_' + postId).hide()
                $('#unsubscribe_' + postId).show()
            }
        }
    });
}

function unSubscribeMe(postId, csrfToken)
{
    url = "/post/" + postId +"/unsubscribe";
    $.ajax({
        url: url,
        type: "POST",
        data: {  csrfmiddlewaretoken: csrfToken, //django needs this
                 data_item: {'post_id':postId}},
        timeout:0,
        success: function(data){
            if(data.result == true) {
                $('#subscribe_' + postId).show()
                $('#unsubscribe_' + postId).hide()
            }
        }
    });
}

function save_tag(postId, csrfToken)
{
    let selectedTagChoice = $('#tag_' + postId).val();
    let url = "/post/" + postId +"/tags/new";

    $.ajax({
        url: url,
        type: "POST",
        data: {  csrfmiddlewaretoken: csrfToken, //django needs this
                 data_item: {'choice':selectedTagChoice}},
        timeout:0,
        success: function(data){
            if(data.result == true) {
                $('#div_tag_' + postId).hide()
                location.reload();
            }
        }
    });
}

function delete_tag(postId, tagId, csrfToken)
{
    let url = "/tags/" + tagId +"/delete";

    $.ajax({
        url: url,
        type: "POST",
        data: {  csrfmiddlewaretoken: csrfToken, //django needs this
              },
        timeout:0,
        success: function(data){
            if(data.result == true) {
                $('#tag_' + postId + '_' + tagId).hide()
            }
        }
    });
}


function save_comment(postId, csrfToken)
{
var comment = $('#txt_comment_' + postId).val();
var is_anonymous = $('#chk_anonymous_' + postId).is(":checked");
console.info('is_anonymous', is_anonymous);


$.ajax({
    type: "POST",
    url: "/post/" + postId + "/comments/new2",
    data:
    {
      csrfmiddlewaretoken: csrfToken,      //django needs this
      data_item:
      {
        'post_id' : postId,
        'content' : comment,
        'anonymous' : is_anonymous
      }
    },
    timeout:0,


     // beforeSend: function(data)
     // {
     //     console.info('$("#loader")', $("#loader"));
     //     $("#loader").show();
     //     //alert('wait');
     // },

    success: function(data)
    {
      if(data.result == true)
      {
          $('#div_comment_box_' + postId).hide();
          $('#comments_container_' + postId).prepend('<div id="comment_detail_' + data.comment.id + '" >');
          $('#comment_detail_' + data.comment.id).load('/comment/' + data.comment.id + '?editable=true');
          $("#txt_comment_"+ postId).val("");

      }
    }
      // complete:function()
      // {
      //    $("#text_comment_"+ postId).value = null;
      // }
  });

}




function edit_comment(commentId,  csrfToken)
{
    var comment = $('#edit_txt_comment_' + commentId).val();
    var is_anonymous = $('#edit_chk_anonymous_' + commentId).is(":checked");

    let url = "/comment/" + commentId + "/update";
    let spinner = $('#spinner_comment_edit_' + commentId);
    spinner.show();

    $.ajax({
        type: "POST",
        url: url,
        data:
        {
          csrfmiddlewaretoken: csrfToken,      //django needs this
          data_item:
          {
            'content' : comment,
            'anonymous' : is_anonymous
          }
        },
        timeout:0,
        success: function(data)
        {
          spinner.hide();
          if(data.result == true)
          {
              hide_me('div_edit_comment_box_' + commentId);
              show_me('p_' + commentId);
              reset_comment_details(commentId, comment, is_anonymous, data);
          }
        }
      });
}


function delete_comment(commentId, csrfToken)
{
    let url = "/comment/" + commentId + "/delete";
    let spinner = $('#spinner_comment_edit_' + commentId);
    spinner.show();
    $.ajax({
        type: "POST",
        url: url,
        data:
        {
          csrfmiddlewaretoken: csrfToken     //django needs this
        },
        timeout:0,
        success: function(data)
        {
          spinner.hide();
          if(data.result == true)
          {

              $('#comment_detail_' + commentId).remove();
               $(".modal-backdrop").remove();
          }
        }
      });
}

function reset_comment_details(commentId, comment, current_anonymous, data)
{
    $('#p_' + commentId).text(comment);
    $('#date_' + commentId).text(data.date_posted);

    if(current_anonymous != data.prev_anonymous)
    {
        let image_src = (current_anonymous == true) ? '/media/profile_pics/anonymous.png' : data.author_profile_pic;
        $('#img_comment_profile_' + commentId).attr('src', image_src);


        if(current_anonymous == true)
        {
            $('#href_user_comment_' + commentId).text('Anonymous User');
            $('#href_user_comment_' + commentId).attr('onclick', 'return false');
            $('#href_user_comment_' + commentId).removeAttr('href');
            $('#href_user_comment_' + commentId).removeAttr('class');
        }
        else
        {
            $('#href_user_comment_' + commentId).text(data.author_name);
            $('#href_user_comment_' + commentId).removeAttr('onclick');
            $('#href_user_comment_' + commentId).attr('href', '/user/' + data.author_name);
            $('#href_user_comment_' + commentId).attr('class', 'mr-2');
        }
    }
}
//
// function open_modal()
// {
//     $('#modal01').style.display='block'
//
// }
//
// function xyz()
// {
//     hide_me('div_edit_comment_box_{{ comment.id}}');
//     show_me('p_{{ comment.id }}');
// }

function setElementVisibilityByPatternStarting(pattern, is_set_visible)
{
    if(is_set_visible) {
        let elements = $("[id^='" + pattern + "']");
        elements.show();
        //elements[0].scrollIntoView(); - scroll without animation

        $('body, html').animate({scrollTop: elements[0].offsetTop}, 500, 'linear');
    }
    else
        $("[id^='" + pattern + "']").hide();
}

function delete_selected_comments(postId, csrfToken)
{
    $("[id^='div_comment_checkbox_" +postId+"'] input:checked").each(function(){
        //selectedCommentIds.push($(this).data('comment-id'));
        delete_comment($(this).data('comment-id'), csrfToken);
    });
    hide_me(`div_delete_selected_${ postId }`);
    setElementVisibilityByPatternStarting(`div_comment_checkbox_${ post.id }`, false);
}






