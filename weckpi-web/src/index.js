import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function submitData() {
    let data = {
        'alarmtimes': {
            'override': {
                'active': document.getElementById('override.active').checked,
                'time': document.getElementById('override.time').value,
                'music': {
                    'type': document.getElementById('override.music.type').value,
                    'url': document.getElementById('override.music.url').value
                }
            },
            'Mon': {
                'active': document.getElementById('Mon.active').checked,
                'time': document.getElementById('Mon.time').value,
                'music': {
                    'type': document.getElementById('Mon.music.type').value,
                    'url': document.getElementById('Mon.music.url').value
                }
            },
            'Tue': {
                'active': document.getElementById('Tue.active').checked,
                'time': document.getElementById('Tue.time').value,
                'music': {
                    'type': document.getElementById('Tue.music.type').value,
                    'url': document.getElementById('Tue.music.url').value
                }
            },
            'Wed': {
                'active': document.getElementById('Wed.active').checked,
                'time': document.getElementById('Wed.time').value,
                'music': {
                    'type': document.getElementById('Wed.music.type').value,
                    'url': document.getElementById('Wed.music.url').value
                }
            },
            'Thu': {
                'active': document.getElementById('Thu.active').checked,
                'time': document.getElementById('Thu.time').value,
                'music': {
                    'type': document.getElementById('Thu.music.type').value,
                    'url': document.getElementById('Thu.music.url').value
                }
            },
            'Fri': {
                'active': document.getElementById('Fri.active').checked,
                'time': document.getElementById('Fri.time').value,
                'music': {
                    'type': document.getElementById('Fri.music.type').value,
                    'url': document.getElementById('Fri.music.url').value
                }
            },
            'Sat': {
                'active': document.getElementById('Sat.active').checked,
                'time': document.getElementById('Sat.time').value,
                'music': {
                    'type': document.getElementById('Sat.music.type').value,
                    'url': document.getElementById('Sat.music.url').value
                }
            },
            'Sun': {
                'active': document.getElementById('Sun.active').checked,
                'time': document.getElementById('Sun.time').value,
                'music': {
                    'type': document.getElementById('Sun.music.type').value,
                    'url': document.getElementById('Sun.music.url').value
                }
            }
        }
    };
    fetch('/scripts/save.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                alert(data.error);
            } else {
                alert('Speichern abgeschlossen!');
            }
        })
        .catch((error) => {
            alert(error);
        })
}

function MainUI(props) {
    const [visibleTab, setVisibleTab] = useState('times');
    const [isLoaded, setIsLoaded] = useState(false);
    const [error, setError] = useState(null);
    const [defaults, setDefaults] = useState([]);

    useEffect(() => {
        fetch("/scripts/load.php")
        .then(res => res.json())
        .then((result) => {
                setDefaults(result);
                setIsLoaded(true);
            }, (error) => {
                setError(error);
                setIsLoaded(true);
            }
        )
    }, [])

    if (error) {
        console.error("An error occured: " + error.message)
        return <div>An error occured. More information in the developer console.</div>;
    } else if (!isLoaded) {
        return <div>Please wait...</div>;
    } else {
        return (
            <>
                <MainMenu entries={menu_entries} title='Weckpi Settings' title_icon='/img/weckpi-logo192.png' setVisibleTab={setVisibleTab} visibleTab={visibleTab}/>
                <TabTimes visibility={visibleTab === 'times'} defaults={defaults}/>
                <TabTimeTemplates visibility={visibleTab === 'time_templates'} defaults={defaults}/>
            </>
        );
    }
}

function Card(props) {
    return(
        <div className='card' style={{width: props.width, height: props.height}}>
            {props.children}
        </div>
    );
}

function TimeCard(props) {
    return(
        <Card width='200px' height='300px'>
            <span className='card-title'>{props.title}</span><br />
            <CheckBox id={props.id + '.active'} checked={props.active}>Wecker aktivieren</CheckBox>
            <input id={props.id + '.time'} type='time' defaultValue={props.time}/>
            <br /><br /><span><b>Musik</b></span>
            <select id={props.id + '.music.type'} defaultValue={props.music.type}>
                <option value='playlist'>Playlist</option>
                <option value='playlist-random'>Playlist (Zufällig)</option>
                <option value='internetradio'>Internetradio</option>
            </select><br /><br />
            <input id={props.id + '.music.url'} type='text' defaultValue={props.music.url} style={{width: '90%'}}/>
        </Card>
    );
}

function Modal(props) {
    return(
        <div className={props.visibility ? 'modal-overlay modal-shown' : 'modal-overlay modal-hidden'}>
            <div className='modal-content' style={{width: props.width, height: props.height}}>
                <p>{props.children}</p>
            </div>
        </div>
    );
}

/*function NotificationBox(props) {
    const [time, setTime] = useState(10);
    let color, color2, img;

    useEffect(() => {
        const timer = setTimeout(() => {
            setTime(time - 1);
        }, 1000);
    });

    switch(props.type) {
        case "error":
            color = "#c70000";
            color2 = "#d99292";
            img = "img/error.svg";
            break;
        case "warning":
            color = "#ffcc33";
            color2 = "#ffe494";
            img = "img/warning.svg";
            break;
        case "success":
            color = "#00aa55";
            color2 = "#00f57a";
            img = "img/success.svg";
            break;
        case "info":
        default:
            color = "#00aa55";
            color = "#00f57a";
            img = "img/info.svg";
            break;
    }

    if(time >= 0) {
        return(
            <div className='notification-box' style={{backgroundColor: color, bottom: props.id * 60 + "px"}}>
                <div className='notification-box2' style={{backgroundColor: color2,  width: 10 * time + "%"}} />
                <img src={img} alt=""/>
                <span title={props.children}>{props.children}</span>
            </div>
        );
    } else {
        props.notifications.splice(props.id, 1);
        return null;
    }
}

function NotificationBoxesContainer(props) {
    const [notifications, setNotifications] = useState([]);
    const notificationBoxes = notifications.map((entry) => <NotificationBox type={entry.type} id={entry.id} notifications={notifications}>{entry.text}</NotificationBox>);    

    newNotification = (type, text) => {
        if(notifications.length === 0) {
            setNotifications([{id: notifications.length, type: type, text: text}]);
        } else {        
            setNotifications([...notifications.values(), {id: notifications.length, type: type, text: text}]);
        }
        console.log(notifications)
    }

    return(
        <>{notificationBoxes}</>
    );
}*/


function CheckBox(props) {
    const [checked, setState] = useState(props.checked);

    return(
        <>
            <input id={props.id} type='checkbox' defaultChecked={checked} onClick={() => {setState(!checked);}}/>
            <label className='checkbox-label' onClick={() => {setState(!checked);}}>{props.children}</label>
        </>
    );
}

function MainMenu(props){
    const entries = props.entries.map((entry) =>
        <MenuEntry icon={entry.icon} tabname={entry.tabname} setVisibleTab={props.setVisibleTab} visibleTab={props.visibleTab}>{entry.text}</MenuEntry>
    );

    return(
        <div className='menu-container'>
            <div className='menu-title'>
                <img src={props.title_icon} alt='' className='menu-icon'/>
                <span className='menu-text'>{props.title}</span>
            </div>
            {entries}
        </div>
    );
}

function MenuEntry(props) {
    return(
        <div className={(props.visibleTab === props.tabname) ? 'menu-entry menu-entry-open' : 'menu-entry'} onClick={() => props.setVisibleTab(props.tabname)}>
            <img src={props.icon} alt='' className='menu-icon'/>
            <span className='menu-text'>{props.children}</span>
        </div>
    );
}

function TabTimes(props) {
    const [loadTemplateVisibility, setLoadTemplateVisibility] = useState(false);

    return(
        <>
            <div className={props.visibility ? 'tab-container tab-container-shown' : 'tab-container tab-container-hidden'}>
                <button className='button' onClick={() => {setLoadTemplateVisibility(true)}}>Vorlage laden... </button>
                <br />
                <TimeCard title='Überschreiben' id='override' active={props.defaults.alarmtimes.override.active} time={props.defaults.alarmtimes.override.time} music={props.defaults.alarmtimes.override.music}/>
                <div className='card-container'>
                    <TimeCard title='Montag' id='Mon' active={props.defaults.alarmtimes.Mon.active} time={props.defaults.alarmtimes.Mon.time} music={props.defaults.alarmtimes.Mon.music}/>
                    <TimeCard title='Dienstag' id='Tue' active={props.defaults.alarmtimes.Tue.active} time={props.defaults.alarmtimes.Tue.time} music={props.defaults.alarmtimes.Tue.music}/>
                    <TimeCard title='Mittwoch' id='Wed' active={props.defaults.alarmtimes.Wed.active} time={props.defaults.alarmtimes.Wed.time} music={props.defaults.alarmtimes.Wed.music}/>
                    <TimeCard title='Donnerstag' id='Thu' active={props.defaults.alarmtimes.Thu.active} time={props.defaults.alarmtimes.Thu.time} music={props.defaults.alarmtimes.Thu.music}/>
                    <TimeCard title='Freitag' id='Fri' active={props.defaults.alarmtimes.Fri.active} time={props.defaults.alarmtimes.Fri.time} music={props.defaults.alarmtimes.Fri.music}/>
                    <TimeCard title='Samstag' id='Sat' active={props.defaults.alarmtimes.Sat.active} time={props.defaults.alarmtimes.Sat.time} music={props.defaults.alarmtimes.Sat.music}/>
                    <TimeCard title='Sonntag' id='Sun' active={props.defaults.alarmtimes.Sun.active} time={props.defaults.alarmtimes.Sun.time} music={props.defaults.alarmtimes.Sun.music}/>
                </div>
                <button onClick={submitData} className='button'>
                Speichern
            </button>
            </div>
            <Modal visibility={loadTemplateVisibility} setVisibility={setLoadTemplateVisibility} height='500px' width='700px'>
                test
            </Modal>
        </>
    );
}

function TabTimeTemplates(props) {
    return(
        <div className={props.visibility ? 'tab-container tab-container-shown' : 'tab-container tab-container-hidden'}>
            <p>Tab Time Templates</p>
        </div>
    );
}

var menu_entries = [
    {
        icon: 'img/times.svg',
        text: 'Weckzeiten',
        tabname: 'times'
    },
    {
        icon: 'img/time_templates.svg',
        text: 'Weckzeiten (Vorlagen)',
        tabname: 'time_templates'
    }
];

ReactDOM.render(<MainUI />, document.getElementById('root'));