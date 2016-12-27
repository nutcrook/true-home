var React = require('react');
var ReactDOM = require('react-dom');
import ReactBootstrapToggle from 'react-bootstrap-toggle';


class Controller extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = ({watts: null, switchedOn: false, temperature: null});
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
       axios.get('http://localhost:9090/devices/' + this.props.id)
            .then(result=> {
                this.setState({watts: result.data[0].watts,
                               switchedOn: result.data[0].status == 1 ? true : false,
                               temperature: result.data[0].temperature});
            });
    }

   triggerSwitch (status) {
       // Temporarily disable the timer
       clearInterval(this.timerID);
       // Make sure the UI is updated
       this.setState({switchedOn: status});

       var request = 'http://localhost:9090/devices/';
       request += this.props.id;
       request += '/';
       request += status ? '1' : '0';
       // Change the state of the real controller
       axios.get(request)
            .then(()=> {
                // Re-enable the timer
                this.timerID = setInterval(
                () => this.tick(),
                2000);
            });
   }

   render() {
        const watts =  null || this.state.watts;
        const switchedOn = this.state.switchedOn;
        const temp = null || this.state.temperature;

        var buttonColStyle = {
            "text-align": "right"
        };

        return (
                 <tr>
                 <td width="90%"><h5 className='controller'>{this.props.name}{ watts != null &&
                 <small> {watts} Watts</small>
                 }{ temp != null &&
                 <small> {parseFloat((temp - 32)*5/9).toFixed(2)} °C</small>
                 }</h5></td>
                 <td style={buttonColStyle}>{this.props.hasStatus && <ReactBootstrapToggle
                     key={this.props.id}
                     on="ON"
                     off="OFF"
                     active={switchedOn}
                     size="mini" onstyle="success" offstyle="danger"
                     onChange={()=> this.triggerSwitch(!switchedOn).bind(this)}/>}</td></tr>

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
    axios.get('http://localhost:9090/devices/by-room/' + this.props.id)
            .then(result=> {
                this.setState({controllers:result.data});
            });
    }

    render() {
        var tableStyle = {
            padding: "10px",
            width: "90vw"
        };


        return (
                <div>
                    <h3>{this.props.name}</h3>
                    <table className="table table-sm" style={tableStyle}><tbody>
                    {this.state.controllers.map(function(controller){
                     return <Controller name={controller.name} id={controller.id} key={controller.id}
                     hasStatus={controller.status != null ? true : false}/>;
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
                    <h1>TrueHome</h1>
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
        axios.get('http://localhost:9090/rooms')
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
               <div>
                   <Header/>
                   <Body/>
               </div>
       );
   }
}


ReactDOM.render(<Content/>, document.getElementById('root'));
