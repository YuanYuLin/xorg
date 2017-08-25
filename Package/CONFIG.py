import ops
import iopc

pkg_path = ""
output_dir = ""
arch = ""
src_lib_dir = ""
dst_lib_dir = ""
src_usr_lib_dir = ""
dst_usr_lib_dir = ""
src_usr_bin_dir = ""
dst_usr_bin_dir = ""
src_usr_sbin_dir = ""
dst_usr_sbin_dir = ""
src_usr_lib_xorg_modules_dir = ""
dst_usr_lib_xorg_modules_dir = ""
src_usr_lib_xorg_modules_drivers_dir = ""
dst_usr_lib_xorg_modules_drivers_dir = ""
src_usr_lib_xorg_modules_input_dir = ""
dst_usr_lib_xorg_modules_input_dir = ""
src_usr_share_dir = ""
dst_usr_share_dir = ""
src_usr_include_dir = ""
dst_usr_include_dir = ""
pkg_tarball = ""
pkg_sysroot_tarball = ""
pkg_tarball_dir = ""
pkg_sysroot_tarball_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global arch
    global src_lib_dir
    global dst_lib_dir
    global src_usr_lib_dir
    global dst_usr_lib_dir
    global src_usr_bin_dir
    global dst_usr_bin_dir
    global src_usr_sbin_dir
    global dst_usr_sbin_dir
    global src_usr_lib_xorg_modules_dir
    global dst_usr_lib_xorg_modules_dir
    global src_usr_lib_xorg_modules_drivers_dir
    global dst_usr_lib_xorg_modules_drivers_dir
    global src_usr_lib_xorg_modules_input_dir
    global dst_usr_lib_xorg_modules_input_dir
    global src_usr_share_dir
    global dst_usr_share_dir
    global src_usr_include_dir
    global dst_usr_include_dir
    global pkg_tarball
    global pkg_sysroot_tarball
    global pkg_tarball_dir
    global pkg_sysroot_tarball_dir

    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    pkg_tarball = ops.path_join(pkg_path, "xorg.tar.xz")
    if arch == "armhf":
        src_lib_dir = iopc.getBaseRootFile("lib/arm-linux-gnueabihf")
        pkg_tarball = ops.path_join(pkg_path, "xorg_armhf.tar.xz")
    elif arch == "armel":
        src_lib_dir = iopc.getBaseRootFile("lib/arm-linux-gnueabi")
        pkg_tarball = ops.path_join(pkg_path, "xorg_armel.tar.xz")
        pkg_sysroot_tarball = ops.path_join(pkg_path, "xorg_armel_sysroot.tar.xz")
    elif arch == "x86_64":
        src_lib_dir = iopc.getBaseRootFile("lib/x86_64-linux-gnu")
        pkg_tarball = ops.path_join(pkg_path, "xorg_x86_64.tar.xz")
        pkg_sysroot_tarball = ops.path_join(pkg_path, "xorg_x86_64_sysroot.tar.xz")
    else:
        sys.exit(1)

    dst_lib_dir = ops.path_join(output_dir, "lib")

    pkg_tarball_dir = ops.path_join(output_dir, "target")
    pkg_sysroot_tarball_dir = ops.path_join(output_dir, "sysroot")

    src_usr_lib_dir = ops.path_join(pkg_tarball_dir, "usr/lib")
    dst_usr_lib_dir = ops.path_join(output_dir, "usr/lib")

    src_usr_bin_dir = ops.path_join(pkg_tarball_dir, "usr/bin")
    dst_usr_bin_dir = ops.path_join(output_dir, "usr/bin")

    src_usr_sbin_dir = ops.path_join(pkg_tarball_dir, "usr/sbin")
    dst_usr_sbin_dir = ops.path_join(output_dir, "usr/sbin")

    src_usr_lib_xorg_modules_dir = ops.path_join(pkg_tarball_dir, "usr/lib/xorg/modules")
    dst_usr_lib_xorg_modules_dir = ops.path_join(output_dir, "usr/lib/xorg/modules")

    src_usr_lib_xorg_modules_drivers_dir = ops.path_join(pkg_tarball_dir, "usr/lib/xorg/modules/drivers")
    dst_usr_lib_xorg_modules_drivers_dir = ops.path_join(output_dir, "usr/lib/xorg/modules/drivers")

    src_usr_lib_xorg_modules_input_dir = ops.path_join(pkg_tarball_dir, "usr/lib/xorg/modules/input")
    dst_usr_lib_xorg_modules_input_dir = ops.path_join(output_dir, "usr/lib/xorg/modules/input")

    src_usr_share_dir = ops.path_join(pkg_tarball_dir, "usr/share")
    dst_usr_share_dir = ops.path_join(output_dir, "usr/share")

    src_usr_include_dir = ops.path_join(pkg_sysroot_tarball_dir, "usr/include")
    dst_usr_include_dir = ops.path_join(output_dir, "usr/include")

    src_include_dir = iopc.getBaseRootFile("usr/include/selinux")
    dst_include_dir = ops.path_join("include",args["pkg_name"])


def MAIN_ENV(args):
    set_global(args)

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.unTarXz(pkg_tarball, output_dir)
    ops.unTarXz(pkg_sysroot_tarball, output_dir)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(output_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)
    return False

def install_package_xeyes(args):
    ops.copyto(ops.path_join(src_usr_bin_dir, "xeyes"), dst_usr_bin_dir)

    ops.copyto(ops.path_join(src_usr_lib_dir, "libXext.so.6.4.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libXext.so.6.4.0", "libXext.so.6.4")
    ops.ln(dst_usr_lib_dir, "libXext.so.6.4.0", "libXext.so.6")
    ops.ln(dst_usr_lib_dir, "libXext.so.6.4.0", "libXext.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libXmu.so.6.2.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libXmu.so.6.2.0", "libXmu.so.6.2")
    ops.ln(dst_usr_lib_dir, "libXmu.so.6.2.0", "libXmu.so.6")
    ops.ln(dst_usr_lib_dir, "libXmu.so.6.2.0", "libXmu.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libXt.so.6.0.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libXt.so.6.0.0", "libXt.so.6.0")
    ops.ln(dst_usr_lib_dir, "libXt.so.6.0.0", "libXt.so.6")
    ops.ln(dst_usr_lib_dir, "libXt.so.6.0.0", "libXt.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libXrender.so.1.3.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libXrender.so.1.3.0", "libXrender.so.1.3")
    ops.ln(dst_usr_lib_dir, "libXrender.so.1.3.0", "libXrender.so.1")
    ops.ln(dst_usr_lib_dir, "libXrender.so.1.3.0", "libXrender.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libSM.so.6.0.1"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libSM.so.6.0.1", "libSM.so.6.0")
    ops.ln(dst_usr_lib_dir, "libSM.so.6.0.1", "libSM.so.6")
    ops.ln(dst_usr_lib_dir, "libSM.so.6.0.1", "libSM.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libICE.so.6.3.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libICE.so.6.3.0", "libICE.so.6.3")
    ops.ln(dst_usr_lib_dir, "libICE.so.6.3.0", "libICE.so.6")
    ops.ln(dst_usr_lib_dir, "libICE.so.6.3.0", "libICE.so")

def MAIN_BUILD(args):
    set_global(args)

    ops.mkdir(dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "cvt"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-cache"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-cat"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-list"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-match"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-pattern"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-query"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-scan"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "fc-validate"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "gtf"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "mcookie"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "xkbcomp"), dst_usr_bin_dir)
    ops.copyto(ops.path_join(src_usr_bin_dir, "Xorg"), dst_usr_bin_dir)
    ops.ln(dst_usr_bin_dir, "Xorg", "X")

    ops.mkdir(dst_usr_lib_dir)
    ops.copyto(ops.path_join(src_usr_lib_dir, "libsha1.so.0.0.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libsha1.so.0.0.0", "libsha1.so.0.0")
    ops.ln(dst_usr_lib_dir, "libsha1.so.0.0.0", "libsha1.so.0")
    ops.ln(dst_usr_lib_dir, "libsha1.so.0.0.0", "libsha1.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libpciaccess.so.0.11.1"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libpciaccess.so.0.11.1", "libpciaccess.so.0.11")
    ops.ln(dst_usr_lib_dir, "libpciaccess.so.0.11.1", "libpciaccess.so.0")
    ops.ln(dst_usr_lib_dir, "libpciaccess.so.0.11.1", "libpciaccess.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libdrm.so.2.4.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libdrm.so.2.4.0", "libdrm.so.2.4")
    ops.ln(dst_usr_lib_dir, "libdrm.so.2.4.0", "libdrm.so.2")
    ops.ln(dst_usr_lib_dir, "libdrm.so.2.4.0", "libdrm.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libpixman-1.so.0.34.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libpixman-1.so.0.34.0", "libpixman-1.so.0.34")
    ops.ln(dst_usr_lib_dir, "libpixman-1.so.0.34.0", "libpixman-1.so.0")
    ops.ln(dst_usr_lib_dir, "libpixman-1.so.0.34.0", "libpixman-1.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libXfont2.so.2.0.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libXfont2.so.2.0.0", "libXfont2.so.2.0")
    ops.ln(dst_usr_lib_dir, "libXfont2.so.2.0.0", "libXfont2.so.2")
    ops.ln(dst_usr_lib_dir, "libXfont2.so.2.0.0", "libXfont2.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libfontenc.so.1.0.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libfontenc.so.1.0.0", "libfontenc.so.1.0")
    ops.ln(dst_usr_lib_dir, "libfontenc.so.1.0.0", "libfontenc.so.1")
    ops.ln(dst_usr_lib_dir, "libfontenc.so.1.0.0", "libfontenc.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libfreetype.so.6.13.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libfreetype.so.6.13.0", "libfreetype.so.6.13")
    ops.ln(dst_usr_lib_dir, "libfreetype.so.6.13.0", "libfreetype.so.6")
    ops.ln(dst_usr_lib_dir, "libfreetype.so.6.13.0", "libfreetype.so.6")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libXau.so.6.0.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libXau.so.6.0.0", "libXau.so.6.0")
    ops.ln(dst_usr_lib_dir, "libXau.so.6.0.0", "libXau.so.6")
    ops.ln(dst_usr_lib_dir, "libXau.so.6.0.0", "libXau.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libXdmcp.so.6.0.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libXdmcp.so.6.0.0", "libXdmcp.so.6.0")
    ops.ln(dst_usr_lib_dir, "libXdmcp.so.6.0.0", "libXdmcp.so.6")
    ops.ln(dst_usr_lib_dir, "libXdmcp.so.6.0.0", "libXdmcp.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libfontconfig.so.1.9.2"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libfontconfig.so.1.9.2", "libfontconfig.so.1.9")
    ops.ln(dst_usr_lib_dir, "libfontconfig.so.1.9.2", "libfontconfig.so.1")
    ops.ln(dst_usr_lib_dir, "libfontconfig.so.1.9.2", "libfontconfig.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libexpat.so.1.6.2"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libexpat.so.1.6.2", "libexpat.so.1.6")
    ops.ln(dst_usr_lib_dir, "libexpat.so.1.6.2", "libexpat.so.1")
    ops.ln(dst_usr_lib_dir, "libexpat.so.1.6.2", "libexpat.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libX11.so.6.3.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libX11.so.6.3.0", "libX11.so.6.3")
    ops.ln(dst_usr_lib_dir, "libX11.so.6.3.0", "libX11.so.6")
    ops.ln(dst_usr_lib_dir, "libX11.so.6.3.0", "libX11.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libxkbfile.so.1.0.2"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libxkbfile.so.1.0.2", "libxkbfile.so.1.0")
    ops.ln(dst_usr_lib_dir, "libxkbfile.so.1.0.2", "libxkbfile.so.1")
    ops.ln(dst_usr_lib_dir, "libxkbfile.so.1.0.2", "libxkbfile.so")

    ops.copyto(ops.path_join(src_usr_lib_dir, "libxcb.so.1.1.0"), dst_usr_lib_dir)
    ops.ln(dst_usr_lib_dir, "libxcb.so.1.1.0", "libxcb.so.1.1")
    ops.ln(dst_usr_lib_dir, "libxcb.so.1.1.0", "libxcb.so.1")
    ops.ln(dst_usr_lib_dir, "libxcb.so.1.1.0", "libxcb.so")

    ops.mkdir(dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libexa.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libfb.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libfbdevhw.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libint10.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libshadow.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libshadowfb.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libvbe.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libvgahw.so"), dst_usr_lib_xorg_modules_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_dir, "libwfb.so"), dst_usr_lib_xorg_modules_dir)

    ops.mkdir(dst_usr_lib_xorg_modules_drivers_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_drivers_dir, "dummy_drv.so"), dst_usr_lib_xorg_modules_drivers_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_drivers_dir, "fbdev_drv.so"), dst_usr_lib_xorg_modules_drivers_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_drivers_dir, "fbturbo_drv.so"), dst_usr_lib_xorg_modules_drivers_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_drivers_dir, "modesetting_drv.so"), dst_usr_lib_xorg_modules_drivers_dir)

    ops.mkdir(dst_usr_lib_xorg_modules_input_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_input_dir, "joystick_drv.so"), dst_usr_lib_xorg_modules_input_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_input_dir, "kbd_drv.so"), dst_usr_lib_xorg_modules_input_dir)
    ops.copyto(ops.path_join(src_usr_lib_xorg_modules_input_dir, "mouse_drv.so"), dst_usr_lib_xorg_modules_input_dir)

    ops.mkdir(dst_usr_share_dir)
    ops.copyto(ops.path_join(src_usr_share_dir, "X11"), dst_usr_share_dir)
    ops.copyto(ops.path_join(src_usr_share_dir, "fontconfig"), dst_usr_share_dir)
    ops.copyto(ops.path_join(src_usr_share_dir, "fonts"), dst_usr_share_dir)
    ops.copyto(ops.path_join(src_usr_share_dir, "xcb"), dst_usr_share_dir)
    ops.copyto(ops.path_join(src_usr_share_dir, "locale"), dst_usr_share_dir)

    ops.mkdir(ops.path_join(dst_usr_share_dir, "fonts/X11"))
    ops.copyto(ops.path_join(src_usr_share_dir, "fonts/X11/100dpi"), ops.path_join(dst_usr_share_dir, "fonts/X11"))
    ops.copyto(ops.path_join(src_usr_share_dir, "fonts/X11/75dpi"), ops.path_join(dst_usr_share_dir, "fonts/X11"))
    ops.copyto(ops.path_join(src_usr_share_dir, "fonts/X11/cyrillic"), ops.path_join(dst_usr_share_dir, "fonts/X11"))
    ops.copyto(ops.path_join(src_usr_share_dir, "fonts/X11/encodings"), ops.path_join(dst_usr_share_dir, "fonts/X11"))
    ops.copyto(ops.path_join(src_usr_share_dir, "fonts/X11/misc"), ops.path_join(dst_usr_share_dir, "fonts/X11"))

    ops.mkdir(dst_usr_include_dir)
    ops.copyto(ops.path_join(src_usr_include_dir, "xcb"), dst_usr_include_dir)

    install_package_xeyes(args)

    return True

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_lib_dir, "."), "usr/lib")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_bin_dir, "."), "usr/bin")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_share_dir, "."), "usr/share")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_include_dir, "."), "include")

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)
    return False

def MAIN(args):
    set_global(args)

