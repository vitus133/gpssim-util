FROM registry.fedoraproject.org/fedora:39

ENV NAME=fedora-hackrf VERSION=39
ENV LD_LIBRARY_PATH=/usr/local/lib
LABEL name="$NAME" \
      version="$VERSION" \
      usage="This image is meant to be used with hackrf" \
      summary="Base image for creating Fedora hackrf containers"

RUN yum -y install wget blas libtool libusb1-devel fftw-devel cmake3 boost-devel git
COPY . /usr/local/bin
COPY brdc1240.24n /

RUN export HACKRF_VERSION="v2023.01.1" \
&& git clone --branch $HACKRF_VERSION --depth 1 https://github.com/greatscottgadgets/hackrf /tmp/hackrf-$HACKRF_VERSION \
&& cmake3 -Wno-dev -S /tmp/hackrf-$HACKRF_VERSION/host -B /tmp/build_hackrf \
&& make -j$(nproc) -C /tmp/build_hackrf \
&& make -C /tmp/build_hackrf install \
&& git clone --branch master --depth 1 https://github.com/osqzss/gps-sdr-sim.git /tmp/gps-sdr-sim \
&& gcc /tmp/gps-sdr-sim/gpssim.c -lm -O3 -o /usr/local/bin/gps-sdr-sim -DUSER_MOTION_SIZE=86400