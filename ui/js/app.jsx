var Hello = React.createClass({
  render: function(){
    return (
      <div>
        <div> May the force be with you </div>
      </div>
    )
  }
});

React.render(<Hello />, document.getElementById('app'));
