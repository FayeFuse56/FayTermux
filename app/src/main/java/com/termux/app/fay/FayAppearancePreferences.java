package com.termux.app.fay;

import android.content.Context;
import android.content.SharedPreferences;
import android.net.Uri;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

/**
 * Persisted appearance configuration for FayTermux.
 *
 * A selected image is not rendered until the terminal renderer supports a
 * transparent background independently of glyph opacity.
 */
public final class FayAppearancePreferences {
    private static final String PREFS = "fay_appearance";
    private static final String IMAGE_URI = "background_image_uri";
    private static final String DIM_PERCENT = "background_dim_percent";
    private static final String ENABLED = "background_enabled";

    private FayAppearancePreferences() {}

    private static SharedPreferences prefs(@NonNull Context context) {
        return context.getApplicationContext()
            .getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    public static void setBackgroundImage(@NonNull Context context, @Nullable Uri uri) {
        prefs(context).edit().putString(IMAGE_URI, uri == null ? null : uri.toString()).apply();
    }

    @Nullable
    public static Uri getBackgroundImage(@NonNull Context context) {
        String value = prefs(context).getString(IMAGE_URI, null);
        return value == null || value.isEmpty() ? null : Uri.parse(value);
    }

    public static void setEnabled(@NonNull Context context, boolean enabled) {
        prefs(context).edit().putBoolean(ENABLED, enabled).apply();
    }

    public static boolean isEnabled(@NonNull Context context) {
        return prefs(context).getBoolean(ENABLED, false);
    }

    public static void setDimPercent(@NonNull Context context, int percent) {
        prefs(context).edit().putInt(DIM_PERCENT, Math.max(0, Math.min(100, percent))).apply();
    }

    public static int getDimPercent(@NonNull Context context) {
        return Math.max(0, Math.min(100, prefs(context).getInt(DIM_PERCENT, 45)));
    }
}
