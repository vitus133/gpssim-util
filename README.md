# Generate and play GPS samples for leap-second testing #

## Build and push
```bash
podman build -t quay.io/vgrinber/hackrf -f Containerfile . && podman push quay.io/vgrinber/hackrf
```
## leap event in the past

```bash
podman run -it --privileged --rm -v /home/user1/vgrinber:/data quay.io/vgrinber/hackrf yesterday-61
```

## Positive leap second tonight

```bash
podman run -it --privileged --rm -v /home/user1/vgrinber:/data quay.io/vgrinber/hackrf leap-tonight-61
```

## Negative leap second tonight

```bash
podman run -it --privileged --rm -v /home/user1/vgrinber:/data quay.io/vgrinber/hackrf leap-tonight-59
```