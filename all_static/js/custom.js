$(document).ready(function() {
    // page is now ready, initialize the calendar...
    $('#factoryCalendar').fullCalendar({
        // put your options and callbacks here
        theme: true,
        header: {
          left: 'title',
          center: '',
          right: 'prev,next',
        },
        views: {
        },
        validRange: {
           start: '2017-10-1',
           end: '2017-12-31',
        },
        events: [],
        eventColor: '#378006',
        eventRender: function(event, element, view) {
         if (event.start.getMonth() !== view.start.getMonth()) { return false; }
        },
        dayClick: function() {
            alert('a day has been clicked!');
        },
    // });
    // $('#calendar').fullCalendar('next');
    });
        
});
