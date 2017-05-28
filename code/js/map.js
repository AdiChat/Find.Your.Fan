var countries = {};
var codes = {};
var fans = 0;
var users = {};
var maxRadius = 100;
var COLORS = [
    "#9b59b6" , "#2ecc71" , "#3498db"
  , "#f39c12" , "#d35400" , "#c0392b"
  , "#1abc9c" , "#34495e" , "#16a085"
  , "#e74c3c" , "#ecf0f1" , "#95a5a6"
  , "#27ae60" , "#2980b9" , "#8e44ad"
  , "#2c3e50" , "#f1c40f" , "#e67e22"
  , "#bdc3c7" , "#7f8c8d"
  ];

var fills = { defaultFill: '#00cc66' };

threeLeterCountryCodes.forEach(function (c, i) 
{ 
  fills[c] = COLORS[i % COLORS.length];
});

function createMap(id, data) 
{
    var map = new Datamap({
      element: document.getElementById(id),
      geographyConfig: 
      {
        popupOnHover: false,
        highlightOnHover: false
      },
      fills: fills
    });
    map.bubbles(data, {
      popupTemplate: function(geo, data) {
        return '<div class="hoverinfo">Country: <strong>' + data.country + '</strong><br>Fans: <strong>' + data.fans_country  + '</strong></div>';
      }
    });
}

data.users.forEach(c => {
    users[c.user] = 1;
    c.countryCode = getCountryCode(c.country);
    codes[c.countryCode] = c.country;
    var arr = countries[c.countryCode] = countries[c.countryCode] || []
    arr.push(c);
    if (arr.length > fans) {
        fans = arr.length;
    }
});

var sessionsData = Object.keys(countries).map(c => {
    var country = countries[c];
    var fans_country = country.length;
    var r = maxRadius * fans_country / fans;

    return {
        radius: r > 60 ? 60 : r < 10 ? 10 : r
      , centered: c
      , fans_country: fans_country
      , country: codes[country[0].countryCode]
      , fillKey: c
    };
});

createMap("map", sessionsData);