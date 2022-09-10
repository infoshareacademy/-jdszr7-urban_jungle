import React from 'react'
import Slider from 'react-touch-drag-slider'

// here we are importing some images 
// but the Slider children can be an array of any element nodes, or your own components
import images from './images'
import image1 from './mashroomPhotos/borowik_krolewski_2.jpg'

function MyCarousel() {

  return (
        <Slider
          onSlideComplete={(i) => {
            console.log('finished dragging, current slide is', i)
          }}
          onSlideStart={(i) => {
            console.log('started dragging on slide', i)
          }}
          activeIndex={0}
          threshHold={100}
          transition={0.5}
          scaleOnDrag={true}
        >

          <img src={image1} key='1'></img>
          <img src={image1} key='2'></img>
          <img src={image1} key='3'></img>
          <img src={image1} key='4'></img>
          <img src={image1} key='5'></img>
          {/* {images.map(({ url, title }, index) => (
            <img src={url} key={index} alt={title} />
          ))} */}
        </Slider>
  )
}

export default MyCarousel