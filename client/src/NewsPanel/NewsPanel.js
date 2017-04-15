//import css file
import './NewsPanel.css';
//use _ to use lodash
import _ from 'lodash';

import React from 'react';

import NewsCard from '../NewsCard/NewsCard';

class NewsPanel extends React.Component{
  constructor(){
    super();
    //use state and setState to store the data from the database
    this.state = {news: null};
    /* since we call this.loadMoreNews() in handleScroll(),
    so we have to bind key word this */
    this.handleScroll = this.handleScroll.bind(this);
  }

  //always execute after the constructor method
  componentDidMount(){
    this.loadMoreNews();
    this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
    window.addEventListener('scroll', this.handleScroll);
  }

  handleScroll() {
    let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
    if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
      console.log('Loading more news');
      this.loadMoreNews();
    }
  }

  loadMoreNews(){
    //initiate a RESTful request
    let request = new Request('http://localhost:3000/news', {
      method: 'GET',
      //avoid always getting the same news
      cache: false});

    //use fetch method to call the request
    fetch(request)
      .then((res) => res.json())
      //this news is from the res returned json file
      .then((news) => {
        this.setState({
          news: this.state.news? this.state.news.concat(news) : news,
        });
      });
  }

  renderNews(){
    /*To render multiple items in React, we pass an array of React elements.
    The most common way to build that array is to map over your array of data.
    It's a lambda expression "equals to for iteration" */
    let newsList = this.state.news.map(function(news) {
      return(
        <a className='list-group-item' herf='#'>
          //transmit news detail to the NewsCard as a props, NewsCard will receive the props
          <NewsCard news={news} />;
        </a>
      );
    });

    return(
      <div className='container-fluid'>
        <div className='list-group'>
          {newsList}
        </div>
      </div>
    );
  }

  render(){
    if(this.state.news){
      return(
        <div>
          {this.renderNews()}
        </div>
      );
    } else {
      return(
        <div>
          <div id='msg-app-loading'>
            Loading...
          </div>
        </div>
      );
    }
  }
}

export default NewsPanel;
