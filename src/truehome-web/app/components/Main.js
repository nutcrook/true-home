var React = require('react');
var ReactDOM = require('react-dom');
import injectTapEventPlugin from 'react-tap-event-plugin';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {
    blue800
} from 'material-ui/styles/colors';
import AppBar from 'material-ui/AppBar';
import Toggle from 'material-ui/Toggle';

injectTapEventPlugin();

var instance = axios.create({
  baseURL: '/api',
  timeout: 1000,
  proxy: {
    host: 'truehome-nutcrook.home.dyndns.org',
  }
});

const muiTheme = getMuiTheme({
  palette: {
      primary1Color: blue800,
  },
});

class Controller extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = ({watts: null, status: false, temperature: null, stateSet: false});
    }

    componentWillMount() {
        this.timerID = setInterval(
                () => this.tick(),
                2000
        );
    }
    componentWillUnmount() {
    clearInterval(this.timerID);
   }

   tick() {
       instance.get('/vera/devices/' + this.props.id)
            .then(result=> {
                this.setState({watts: result.data[0].watts,
                               status: result.data[0].status == 1 ? true : false,
                               temperature: result.data[0].temperature,
                               stateSet: true});
            });
    }

   triggerSwitch (status) {
       // Temporarily disable the timer
       clearInterval(this.timerID);
       // Make sure the UI is updated
       this.setState({status: status});

       var request = '/vera/devices/';
       request += this.props.id;
       request += '/';
       request += status ? '1' : '0';
       // Change the state of the real controller
       instance.get(request)
            .then(()=> {
                // Re-enable the timer
                this.timerID = setInterval(
                () => this.tick(),
                2000);
            });
   }

   render() {
        const watts = this.state.stateSet == true ? this.state.watts : this.props.watts;
        const switchedOn = this.state.stateSet == true ? this.state.status : this.props.status;
        const temp =  this.state.stateSet == true ? this.state.temperature : this.props.temperature;

        const styles = {
          thumbSwitched: {
            backgroundColor: '#1565C0',
          },
          thumbOff: {
            backgroundColor: '#D32F2F',
          },
          trackOff: {
            backgroundColor: '#EF9A9A',
          },
          trackSwitched: {
            backgroundColor: '#90CAF9',
          },
          title: {
              width: "100%"
          }
        };

        var buttonColStyle = {
            textAlign: "right"
        };

        return (
                 <tr>
                 <td style={styles.title}><h5 className='controller'>{this.props.name}{ watts != null &&
                 <small> {watts} Watts</small>
                 }{ temp != null &&
                 <small> {parseFloat((temp - 32)*5/9).toFixed(2)} °C</small>
                 }</h5></td>
                 <td style={buttonColStyle}>{this.props.hasStatus && <Toggle
                     toggled={switchedOn}
                     thumbSwitchedStyle={styles.thumbSwitched}
                     trackSwitchedStyle={styles.trackSwitched}
                     onToggle={()=> this.triggerSwitch(!switchedOn).bind(this)}/>}</td></tr>
        );
    }

}

class Room extends React.Component {
    constructor(props)
    {
        super(props);
        this.state = {controllers: []};
    }
    componentDidMount() {
    instance.get('/vera/devices/by-room/' + this.props.id)
            .then(result=> {
                this.setState({controllers:result.data});
            });
    }

    render() {
        var tableStyle = {
            width: "98vw",
            marginLeft: "1vw",
            marginRight: "1vw"
        };


        return (
                <div>
                    <h3 style={{marginLeft: "0.5vw"}}>{this.props.name}</h3>
                    <table className="table table-sm" style={tableStyle}><tbody>
                    {this.state.controllers.map(function(controller){
                     return <Controller name={controller.name}
                                        id={controller.id}
                                        key={controller.id}
                                        hasStatus={controller.status != null ? true : false}
                                        status={controller.status == "1" ? true : false}
                                        watts = {controller.watts}/>;
                    })}</tbody></table>
                </div>
        );
    }
}

class Header extends React.Component
{
    render()
    {
        return (
                <div>
                    <AppBar
                        title="TrueHome"
                        iconClassNameRight="muidocs-icon-navigation-expand-more"/>
                </div>
        );
    }
}

class Body extends React.Component
{
    constructor() {
        super();
        this.state = {rooms: []};
    }

    componentDidMount() {
        instance.get('/vera/rooms')
                .then(result=> {
                    this.setState({rooms:result.data});
                });
    }

    render() {
        return (
                <div>
                    {this.state.rooms.map(function(room){
                     return <Room name={ room.name } id={room.id} key={room.id}/>;
                  })}

                </div>
        );
    }
}

class Content extends React.Component
{
   render()
   {
       return (
           <MuiThemeProvider muiTheme={muiTheme}>
               <div>
                   <Header/>
                   <Body/>
               </div>
           </MuiThemeProvider>
       );
   }
}


ReactDOM.render(<Content/>, document.getElementById('app'));
