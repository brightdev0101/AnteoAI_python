//
//  page.swift
//  Anteo AI
//
//  Created by Mehmet Karaaslan on 8.02.2022.
//  Copyright © 2022 Mehmet Karaaslan. All rights reserved.
//

import SwiftUI
import WebKit

//struct page: UIViewRepresentable {
//
//    typealias UIViewType = WKWebView
//    let webView = WKWebView()
//
//    func makeUIView(context: Context) -> WKWebView {
//
//        guard let url = URL(string: "https://anteo.ai") else {
//            return WKWebView()
//        }
//        let request = URLRequest(url: url)
//        webView.load(request)
//        webView.navigationDelegate = context.coordinator
//        return webView
//    }
//
//    func updateUIView(_ uiView: WKWebView, context: Context) { }
//
//    func makeCoordinator() -> Coordinator {
//        return Coordinator()
//    }
//
//    public func goBack() {
//        webView.goBack()
//    }
//
//    class Coordinator: NSObject, WKNavigationDelegate {
//        func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
//            if let url = navigationAction.request.url {
//                print(url, url.host)
//
//                if url.absoluteString.prefix(24) == "https://anteo.ai/reports" {
//                    print("|----3")
//                    decisionHandler(.cancel)
//                    return
//                }
//
//                if url.host == "anteo.ai" {
//                    print("|----1")
//                    decisionHandler(.allow)
//                }
//                else {
//                    print("|----2")
//                    UIApplication.shared.open(url)
//                    decisionHandler(.cancel)
//                }
//            }
//        }
//    }
//}


struct WebView: UIViewRepresentable {
    typealias UIViewType = WKWebView

    let webView: WKWebView
    let shared: Shared
    
    func makeUIView(context: Context) -> WKWebView {
        guard let url = URL(string: "https://anteo.ai") else {
            return WKWebView()
        }
        webView.load(URLRequest(url: url))
        webView.navigationDelegate = context.coordinator
        webView.uiDelegate = context.coordinator
        return webView
    }
    
    func updateUIView(_ uiView: WKWebView, context: Context) { }
    
    func makeCoordinator() -> WebViewDelegate {
        return WebViewDelegate(shared)
    }
}

class WebViewDelegate: NSObject, WKNavigationDelegate, WKUIDelegate {
    let shared: Shared
    
    init(_ shared: Shared) {
        self.shared = shared
    }
    
    
    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        if let url = navigationAction.request.url {
            
            print(url)
            if url.absoluteString.prefix(24) == "https://anteo.ai/reports" {
                print("|----3")
                self.shared.showPdf = true
                decisionHandler(.allow)
                return
            }
            self.shared.showPdf = false
            
            if navigationAction.targetFrame == nil {
                print("|----4")
                decisionHandler(.cancel)
                UIApplication.shared.open(url)
                return
            }
            
            if url.host == "anteo.ai" {
                print("|----1")
                decisionHandler(.allow)
            }
            else {
                print("|----2")
                UIApplication.shared.open(url)
                decisionHandler(.cancel)
            }
        }
    }
    
    //to show alerts
    func webView(_ webView: WKWebView, runJavaScriptAlertPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo,
                 completionHandler: @escaping () -> Void) {
        print("---alert 1")
        shared.alert = Alert(title: Text(message), message: nil, dismissButton: .default(Text("Got It"), action: {}))
        shared.showAlert = true
        completionHandler()
    }


//    func webView(_ webView: WKWebView, runJavaScriptConfirmPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo,
//                 completionHandler: @escaping (Bool) -> Void) {
//        print("---alert 2")
//        shared.showAlert = true
//        print(shared.alertMessage)
//        completionHandler(false)
//
//    }


    func webView(_ webView: WKWebView, runJavaScriptTextInputPanelWithPrompt prompt: String, defaultText: String?, initiatedByFrame frame: WKFrameInfo,
                 completionHandler: @escaping (String?) -> Void) {
        print("---alert 3")
        
        let alert = UIAlertController(title: prompt, message: nil, preferredStyle: .alert)
        alert.addTextField() { textField in
            textField.placeholder = defaultText ?? ""
        }
        alert.addAction(UIAlertAction(title: "Cancel", style: .destructive) {_ in
            completionHandler(nil)
        })
        alert.addAction(UIAlertAction(title: "Done", style: .default) { _ in
            completionHandler(alert.textFields?.first?.text)
        })
        showAlert(alert: alert)
    }
    
    // to show alert with text field
    func showAlert(alert: UIAlertController) {
        if let controller = topMostViewController() {
            controller.present(alert, animated: true)
        }
    }

    private func keyWindow() -> UIWindow? {
        return UIApplication.shared.connectedScenes
        .filter {$0.activationState == .foregroundActive}
        .compactMap {$0 as? UIWindowScene}
        .first?.windows.filter {$0.isKeyWindow}.first
    }

    private func topMostViewController() -> UIViewController? {
        guard let rootController = keyWindow()?.rootViewController else {
            return nil
        }
        return topMostViewController(for: rootController)
    }

    private func topMostViewController(for controller: UIViewController) -> UIViewController {
        if let presentedController = controller.presentedViewController {
            return topMostViewController(for: presentedController)
        } else if let navigationController = controller as? UINavigationController {
            guard let topController = navigationController.topViewController else {
                return navigationController
            }
            return topMostViewController(for: topController)
        } else if let tabController = controller as? UITabBarController {
            guard let topController = tabController.selectedViewController else {
                return tabController
            }
            return topMostViewController(for: topController)
        }
        return controller
    }
}

class WebViewModel: ObservableObject {
    let webView: WKWebView
    
    init() {
        let configuration = WKWebViewConfiguration()
        configuration.websiteDataStore = .default()
        webView = WKWebView(frame: .zero, configuration: configuration)
    }
    
    func goBack() {
        webView.goBack()
    }
}

class Shared: ObservableObject {
    @Published var showPdf = false
    
    @Published var showAlert = false
    @Published var alert = Alert(title: Text("ERROR"), message: nil, dismissButton: .cancel())
}
