'use strict';

const domContainer = document.querySelector('#react_root');
const root = ReactDOM.createRoot(domContainer);

class MyForm extends React.Component
{
  constructor(props)
  {
    super(props);
    this.state = {
      username: String(),
      email: String(),
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
      root.render(
        <h2 style={{display: 'flex', margin: '0 auto'}}>
          Check your email service for confirmation mail
        </h2>
      )
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
          pattern="^[a-zA-Z\d_]{3,25}$"
          required="required"
          placeholder="Username"
          onChange={(e) => this.setState({username: e.target.value})} />
        </div>
        <div className="mb-3">
          <input className="form-control"
          type="email"
          required="required"
          placeholder="Email"
          onChange={(e) => this.setState({email: e.target.value})} />
        </div>
        <div className="mb-3">
          <input className="form-control"
          type="password"
          pattern="^\S{8,30}$"
          required="required"
          placeholder="Password"
          onChange={(e) => this.setState({password: e.target.value})} />
        </div>
        <div className="mb-3 mx-auto">
          <input className="btn btn-primary" type="submit" value="Register" style={{width: 120 + 'px'}}/>
        </div>
      </form>
    )
  }
}

root.render(<MyForm />)