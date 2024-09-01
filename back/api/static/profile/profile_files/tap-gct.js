var thirstyGct;

jQuery( document ).ready( function ($) {

    thirstyGct = {

        trackClick: function () {
            if ( ! window.thirstyFunctions) {
                return;
            }

            if ( tap_gct_vars.ga_func_name === '_gaq.push' ) {
                if ( typeof _gaq == 'undefined' || typeof _gaq.push != 'function' ) {
                    return;
                }
            } else if ( tap_gct_vars.ga_func_name === 'dataLayer.push' ) {
                if ( typeof dataLayer == 'undefined' || typeof dataLayer.push != 'function' ) {
                    return;
                }
            } else if (typeof window[tap_gct_vars.ga_func_name] != 'function') {
                return;
            }

            var $this = $( this ),
                linkID = $this.data( 'linkid' ),
                href = linkID ? $this.attr( 'href' ) : thirstyFunctions.isThirstyLink( $this.attr( 'href' ) );

            if ( ! href ) {
                return;
            }

            var is_uncloak = href.indexOf( tap_gct_vars.home_url + '/' + thirsty_global_vars.link_prefix ) < 0,
                href_parts = href.split('/'),
                href_last = href_parts[ href_parts.length - 1 ] ? href_parts[ href_parts.length - 1 ] : href_parts[ href_parts.length - 2 ],
                link_text = $this.text(),
                link_uri = linkID && is_uncloak ? href : href.replace( tap_gct_vars.home_url , '' ),
                link_slug = linkID && is_uncloak ? href : href_last,
                event_action;

            if ( tap_gct_vars.event_action === 'href' ) {
                event_action = href;
            } else if ( tap_gct_vars.event_action === 'link_text' ) {
                event_action = link_text;
            } else if ( tap_gct_vars.event_action === 'link_slug' ) {
                event_action = link_slug;
            } else {
                event_action = link_uri;
            }

            switch (tap_gct_vars.script_type) {
                case 'gtm':
                    dataLayer.push({ event: tap_gct_vars.action_name, link_uri: event_action });
                    break;
                case 'legacy_ga':
                    _gaq.push( [ '_trackEvent', tap_gct_vars.action_name, event_action, tap_gct_vars.page_slug, undefined, false ] );
                    break;
                case 'universal_ga':
                    window[tap_gct_vars.ga_func_name]( 'send', 'event', {
                        eventCategory: tap_gct_vars.action_name,
                        eventAction: event_action,
                        eventLabel: tap_gct_vars.page_slug,
                        transport: 'beacon'
                    } );
                    break;
                case 'gtag_ga':
                default:
                    gtag( 'event', tap_gct_vars.action_name, {
                        event_category: tap_gct_vars.action_name,
                        event_action: event_action,
                        event_label: tap_gct_vars.page_slug
                    } );
            }
        }

    };

    $( 'body' ).on( 'click', 'a', thirstyGct.trackClick );

    // Backwards compatibility
    window.thirstyGoogleClickTrack = thirstyGct.trackClick;
});
