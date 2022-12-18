const domContainer = document.body;
const root = ReactDOM.createRoot(domContainer);

class API
{
    async isAuthor()
    {
        let url = window.location.href.slice()
        let data = {action: "isauthor"}
        try {
            // запрос
            const response = await fetch(
              url,
              {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {'Content-Type': 'application/json'}
              }
            );
            // ответ
            const json = await response.json();
            console.log('isAuthor:', json["isauthor"]);
            return json["isauthor"];
          }
          catch (error) {
            console.error('Caught error:', error);
          }
    }
}

class TopPanel extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = {
            username: props["username"],
            connection: new API()
        }
    }

    async renderButtons()
    {
        let logout_icon = <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-log-out"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>;
        let edit_icon = <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>;
        let ia = await this.state.connection.isAuthor();
        console.log("renderButtons", ia)
        if (ia)
        {
            return (
                <div className="px-0">
                    <button className="btn p-2 bg-transparent">{edit_icon}</button>
                    <button className="btn p-2 bg-transparent">{logout_icon}</button>
                </div>
            )
        }
        else
        {
            return (
                <div className="px-0">
                    <button className="btn p-2 bg-transparent">{logout_icon}</button>
                </div>
            )
        }
    }

    async render()
    {
        let buttons = await this.renderButtons();
        return (
            <div className="container-fluid d-flex bg-primary bg-gradient justify-content-between rounded-bottom px-0">
                <div className="text-white d-flex align-items-center px-2">
                    <h5 className="my-auto">{this.state.username}</h5>
                </div>
                {buttons}
            </div>
        );
    }
}

let username_read = window.location.pathname.slice(window.location.pathname.lastIndexOf("/")+1);
let panel = new TopPanel({username: username_read})
panel.render().then((elem) => {
    root.render(elem);
});
