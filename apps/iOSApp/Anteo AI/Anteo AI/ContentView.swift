//
//  ContentView.swift
//  Anteo AI
//
//  Created by Mehmet Karaaslan on 8.02.2022.
//  Copyright © 2022 Mehmet Karaaslan. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    
    @State var connected: Bool = isConnected()
    @ObservedObject var shared = Shared()
    @StateObject var model = WebViewModel()
    
    var body: some View {
        VStack {
            if connected {
                //page(model: self.model)
                VStack(alignment: .leading) {
                    if self.shared.showPdf {
                        Button(action: {
                            model.goBack()
                        }, label: {
                            Image(systemName: "arrowshape.turn.up.backward")
                        })
                        .padding(.leading)
                    }
                    
                    WebView(webView: model.webView, shared: self.shared)
                        .alert(isPresented: $shared.showAlert) {
                            shared.alert
                        }
                }
            }
            else {
                GeometryReader { geo in
                    VStack {
                        Image("logo_anteo_ai")
                            .resizable()
                            .scaledToFit()
                            .frame(width: geo.size.width * 0.5)
                            
                        Text("NO CONNECTION")
                        Image(systemName: "wifi.slash").imageScale(.large)
                        Button(action: {
                            if isConnected() {
                                self.connected = true
                            }
                        }) {
                            Image(systemName: "arrow.counterclockwise.circle")
                                .imageScale(.large)
                                .font(.system(size: 30))
                        }.padding()
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .center)
                }
            }
        }.onAppear() {
            _ = Timer.scheduledTimer(withTimeInterval: 5, repeats: true) { _ in
                self.connected = isConnected()
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
