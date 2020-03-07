$(function () {
    $(".js-unfollow_btn").each(function() {
        $(this).click(function() {
            btn = $(this);
            user = $(this).data('unfollow');
            unfollow(user, btn);
        });
    });

    $(".js-follow_btn").each(function() {
        $(this).click(function() {
            btn = $(this);
            user = $(this).data('follow');
            follow(user, btn);
        });
    });

    $(document).on('click', '.js-bookmarkBtn', function() {
        btn = $(this);
        poem = $(this).data('bookmark');
        bookmark(poem, btn);
    });
    
    $(document).on('click', '.js-unbookmarkBtn', function() {
        btn = $(this);
        poem = $(this).data('unbookmark');
        unbookmark(poem, btn);
    });

    $(document).on('click', '.js-removeBtn', function() {
        poem = $(this).data('unbookmark');
        removeBookmark(poem);
    });
    
    $(document).on('click', '#js-follow-profile', function() {
        btn = $('#js-follow-profile');
        user = $(btn).data('follow');
        follow(user, btn);
    });
     
    $(document).on('click', '#js-unfollow-profile', function() {
        btn = $('#js-unfollow-profile');
        user = $(btn).data('unfollow');
        unfollow(user, btn);
    });     

    $(document).on('click', '.js-likeBtn', function() {
        btn = $(this);
        poem = $(this).data('like');
        like(poem, btn);
    });

    $(document).on('click', '.login-alert', function(){
        msg_type = 'info'
        msg = "You need to login to like this poem"
        message(msg, msg_type);
    });

    $(document).on('click', '.js-unlikeBtn', function() {
        btn = $(this);
        poem = $(this).data('unlike');
        unlike(poem, btn);
    });

    $('#js-deletepic').click(function() {        
        cfn = confirm('Are you sure you want to delete your profile picture?');
        if(cfn){
            deleteProfilePic();
        }
    });

    var file_data;
    var file_ext;
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {            
                $('#imagePreview').css('background-image', 'url('+e.target.result +')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
                file_ext = input.files[0].type;
                file_data = e.target.result;
            }
            reader.readAsDataURL(input.files[0]);
        }    
    }
    $("#imageUpload").change(function() {
        readURL(this); 
    });
    $('#js-uploadpic').click(function(){    
        upload_picture(file_ext, file_data)
    });
    
    $(document).on('click', '#js-deletePicBtn', function() {
        user = $(this).data('user');
        deleteProfilePic(user);
    });

    function unfollow(user, btn) {
        $.ajax({
            beforeSend: function() {
                $(btn).addClass('loading disabled'); 
            },
            url: `/ajax/unfollow/${user}`, 
            data: {
                'user': user
            },
            dataType: 'json',
        }).done(function(data) {
            if(data.success){
                $(btn)
                    .removeClass('loading disabled') 
                    .replaceWith(`<div id="js-follow-profile" class="ui mini basic follow button js-follow_btn" data-follow="${user}">Follow</div>`);
            }
            else {
                $(btn).removeClass('loading disabled')
            }
        }).fail(function(){
            $(btn)
                .removeClass('loading disabled');
        });
    }

    function follow(user, btn) {
        $.ajax({
            beforeSend: function() {
                $(btn).addClass('loading disabled'); 
            },
            url: `/ajax/follow/${user}`, 
            data: {
                'user': user
            },
            dataType: 'json',
        }).done(function(data) {
            if(data.success){
                $(btn)
                    .removeClass('loading disabled') 
                    .replaceWith(`<div id="js-unfollow-profile" class="ui mini blue button js-unfollow_btn" data-unfollow="${user}">Unfollow</div>`);
            }
            else {
                $(btn)
                    .removeClass('loading disabled')
            }
        }).fail(function(){
            $(btn)
                .removeClass('loading disabled');
        });
    }

    function bookmark(poem, btn) {
        $.ajax({
            url: `/ajax/bookmark/${poem}`,
            data: {
                'poem': poem
            },
            dataType: 'json',
        }).done(function(data){
            if(data.success) {
                $(btn)
                    .replaceWith(`<i class="right floated bookmark icon js-unbookmarkBtn" data-unbookmark="${poem}"></i>`)                
                msg = 'Poem added to bookmarks successfully!';
                msg_type = 'positive';
                message(msg, msg_type);
            }
        });
    }

    // Unbookmark Function
    function unbookmark(poem, btn) {
        $.ajax({
            url: `/ajax/unbookmark/${poem}`,
            data: {
                'poem': poem
            },
            dataType: 'json',
        }).done(function(data){
            if(data.success) {
                $(btn)
                    .replaceWith(`<i class="right floated bookmark outline icon js-bookmarkBtn" data-bookmark="${poem}"></i>`)                
                msg = 'Poem removed from bookmarks successfully!';
                msg_type = 'positive';
                message(msg, msg_type);                   
            }
        });
    }

    // Like function
    function like(poem, btn) {        
        $.ajax({
            url: `/ajax/like/${poem}`,
            data: {
                'poem': poem
            },
            dataType: 'json',
        }).done(function(data){
            if(data.success) {
                $(btn)
                    .replaceWith(`<i class="heart large icon animate-like-Btn js-unlikeBtn" data-unlike="${poem}"></i>`)                
                $('.likeNum')
                    .text(data.likes);                   
            }
        });
    }

    // Like function
    function unlike(poem, btn) {
        $.ajax({
            url: `/ajax/unlike/${poem}`,
            data: {
                'poem': poem
            },
            dataType: 'json',
        }).done(function(data){
            if(data.success) {
                $(btn)
                    .replaceWith(`<i class="heart outline large icon animate-like-Btn js-likeBtn" data-like="${poem}"></i>`)
                $('.likeNum')
                    .text(data.likes);
            }
        });
    }
    
    // Remove Function
    function removeBookmark(poem) {
        $.ajax({
            url: `/ajax/unbookmark/${poem}`,
            data: {
                'poem': poem
            },
            dataType: 'json',
        }).done(function(data){
            if(data.success) {
                $(`[data-remove=${poem}]`)
                    .transition('fly left');
                                    
                msg = 'Poem removed from bookmarks successfully!';
                msg_type = 'positive';
                message(msg, msg_type);                   
            }
        });
    }

    //Upload Profile Picture
    function upload_picture(file_ext, file_data) {
        $.ajax({
            beforeSend: function() {
                $('#js-uploadpic').addClass('loading disabled'); 
            },
            url: '/ajax/upload_picture',
            type: "POST",
            data: {
                'picture': file_data,
                'ext': file_ext
            },        
            dataType: 'json',
        }).done(function(data){
            if(data.success) {  
                $('#js-uploadpic').removeClass('loading disabled');               
                msg = 'Profile picture updated successfully!'; 
                msg_type = 'positive';
                message(msg, msg_type);
            } else {
                $('#js-uploadpic').removeClass('loading disabled');
                msg = data.error;
                msg_type = 'error';
                message(msg, msg_type);
            }
        }).fail(function(){
                $('#js-uploadpic').removeClass('loading disabled');
                msg = 'Oops! Please, try again!'
                msg_type = 'error';
                message(msg, msg_type);
        });
    }

    //Delete Profile Picture
    function deleteProfilePic() {
        $.ajax({
            beforeSend: function() {
                $('#js-deletepic').addClass('loading disabled');
            },
            url: '/ajax/delete_picture',
            type: "POST",
        }).done(function(data){
            if(data.success) {  
                $('#js-deletepic').removeClass('loading');              
                msg = 'Profile picture removed!';
                msg_type = 'positive'
                message(msg, msg_type);                   
            } else {
                $('#js-deletepic').removeClass('loading disabled');
                msg = 'Oops! Please try again!';
                msg_type = 'error';
                message(msg, msg_type);
            }
        }).fail(function(){
            $('#js-deletepic').removeClass('loading disabled');
            msg = 'Oops!, Please, try again!'
            msg_type = 'error';
            message(msg, msg_type);
        });
    }

    function message(msg, msg_type) {
        div = document.createElement('div')
                $(div).addClass(`ui message ${msg_type}`)
                $(div).text(msg)
                $(div).prepend('<i class="close icon"></i>')
            $('#messageBox').prepend($(div));
            $(div).fadeOut(7000);
    }

});