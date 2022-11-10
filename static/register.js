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
      <form onSubmit={(e) => this.handleSubmit(e)}>
        <input className="reg_input_text"
          type="text"
          placeholder="Username"
          onChange={(e) => this.setState({username: e.target.value})} />
        <input className="reg_input_text"
          type="text"
          placeholder="Email"
          onChange={(e) => this.setState({email: e.target.value})} />
        <input className="reg_input_text"
          type="password"
          placeholder="Password"
          onChange={(e) => this.setState({password: e.target.value})} />
        <input className="reg_input_submit" type="submit" value="Register"/>
      </form>
    )
  }
}

root.render(<MyForm />)