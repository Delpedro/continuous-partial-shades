Continuous Partial Shades
=========================

This is the demo app I used in my CloudConf 2016 talk, [“The Internet is a Computer”](http://video.html.it/aanand-prasad/). It’s an over-engineered but still obnoxiously hacky webapp which puts shades on people’s faces in images (including animated gifs).

To run it, [install the Docker Toolbox](https://www.docker.com/products/docker-toolbox), then:

    $ docker-compose up

After building the images, it will start 3 containers, including a webapp which listens on port 80 on your Docker Machine VM. To get your VM’s IP address, run:

    $ docker-machine ip

Then open that IP in your browser.
