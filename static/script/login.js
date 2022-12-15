'use strict';

const domContainer = document.querySelector('#react_root');
const root = ReactDOM.createRoot(domContainer);

class MyForm extends React.Component
{
  constructor(props)
  {
    super(props);
    this.state = {
      login: String(),
      password: String(),
    };
  }

  async handleSubmit(event)
  {
    const url = window.location.href.slice();
    const data = this.state;
    console.log(url, data);
    event.preventDefault();
    try {
      const response = await fetch(
        url,
        {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {'Content-Type': 'application/json'}
        }
      );

      const json = await response.json();
      console.log('Success:', JSON.stringify(json));
      if (json["success"] == false)
      {
        root.render(
            <h2 style={{display: 'flex', margin: '0 auto'}}>
              Login attempt failed, check your login or password, and try again!
            </h2>
        );
      }
      else
      {
        window.location.href = window.location.origin + "/user/" + json["username"];
      }
    }
    catch (error) {
      console.error('Caught error:', error);
    }
  }

  render()
  {
    return (
      <form onSubmit={(e) => this.handleSubmit(e)} className="container p-1">
        <div className="mb-3">
          <input className="form-control"
          type="text"
          required="required"
          placeholder="Username or email"
          onChange={(e) => this.setState({login: e.target.value})} />
        </div>
        <div className="mb-3">
          <input className="form-control"
          type="password"
          pattern="^\S{8,30}$"
          required="required"
          placeholder="Password"
          onChange={(e) => this.setState({password: e.target.value})} />
        </div>
        <div className="mb-3 mx-auto" style={{width: 120 + 'px'}}>
          <input className="btn btn-primary" type="submit" value="Login" style={{width: 100 + "%"}}/>
        </div>
      </form>
    )
  }
}

root.render(<MyForm />)