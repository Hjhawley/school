// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v3.21.12
// source: chord.proto

package protocol

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.64.0 or later.
const _ = grpc.SupportPackageIsVersion9

const (
	Chord_Ping_FullMethodName                        = "/chord.Chord/Ping"
	Chord_Put_FullMethodName                         = "/chord.Chord/Put"
	Chord_Get_FullMethodName                         = "/chord.Chord/Get"
	Chord_Delete_FullMethodName                      = "/chord.Chord/Delete"
	Chord_GetAll_FullMethodName                      = "/chord.Chord/GetAll"
	Chord_PutAll_FullMethodName                      = "/chord.Chord/PutAll"
	Chord_GetSome_FullMethodName                     = "/chord.Chord/GetSome"
	Chord_Notify_FullMethodName                      = "/chord.Chord/Notify"
	Chord_GetPredecessorAndSuccessors_FullMethodName = "/chord.Chord/GetPredecessorAndSuccessors"
	Chord_FindSuccessor_FullMethodName               = "/chord.Chord/FindSuccessor"
)

// ChordClient is the client API for Chord service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type ChordClient interface {
	Ping(ctx context.Context, in *PingRequest, opts ...grpc.CallOption) (*PingResponse, error)
	Put(ctx context.Context, in *PutRequest, opts ...grpc.CallOption) (*PutResponse, error)
	Get(ctx context.Context, in *GetRequest, opts ...grpc.CallOption) (*GetResponse, error)
	Delete(ctx context.Context, in *DeleteRequest, opts ...grpc.CallOption) (*DeleteResponse, error)
	GetAll(ctx context.Context, in *GetAllRequest, opts ...grpc.CallOption) (*GetAllResponse, error)
	PutAll(ctx context.Context, in *PutAllRequest, opts ...grpc.CallOption) (*PutAllResponse, error)
	GetSome(ctx context.Context, in *GetSomeRequest, opts ...grpc.CallOption) (*GetSomeResponse, error)
	Notify(ctx context.Context, in *NotifyRequest, opts ...grpc.CallOption) (*NotifyResponse, error)
	GetPredecessorAndSuccessors(ctx context.Context, in *GetPredecessorAndSuccessorsRequest, opts ...grpc.CallOption) (*GetPredecessorAndSuccessorsResponse, error)
	FindSuccessor(ctx context.Context, in *FindSuccessorRequest, opts ...grpc.CallOption) (*FindSuccessorResponse, error)
}

type chordClient struct {
	cc grpc.ClientConnInterface
}

func NewChordClient(cc grpc.ClientConnInterface) ChordClient {
	return &chordClient{cc}
}

func (c *chordClient) Ping(ctx context.Context, in *PingRequest, opts ...grpc.CallOption) (*PingResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(PingResponse)
	err := c.cc.Invoke(ctx, Chord_Ping_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) Put(ctx context.Context, in *PutRequest, opts ...grpc.CallOption) (*PutResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(PutResponse)
	err := c.cc.Invoke(ctx, Chord_Put_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) Get(ctx context.Context, in *GetRequest, opts ...grpc.CallOption) (*GetResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(GetResponse)
	err := c.cc.Invoke(ctx, Chord_Get_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) Delete(ctx context.Context, in *DeleteRequest, opts ...grpc.CallOption) (*DeleteResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(DeleteResponse)
	err := c.cc.Invoke(ctx, Chord_Delete_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) GetAll(ctx context.Context, in *GetAllRequest, opts ...grpc.CallOption) (*GetAllResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(GetAllResponse)
	err := c.cc.Invoke(ctx, Chord_GetAll_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) PutAll(ctx context.Context, in *PutAllRequest, opts ...grpc.CallOption) (*PutAllResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(PutAllResponse)
	err := c.cc.Invoke(ctx, Chord_PutAll_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) GetSome(ctx context.Context, in *GetSomeRequest, opts ...grpc.CallOption) (*GetSomeResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(GetSomeResponse)
	err := c.cc.Invoke(ctx, Chord_GetSome_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) Notify(ctx context.Context, in *NotifyRequest, opts ...grpc.CallOption) (*NotifyResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(NotifyResponse)
	err := c.cc.Invoke(ctx, Chord_Notify_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) GetPredecessorAndSuccessors(ctx context.Context, in *GetPredecessorAndSuccessorsRequest, opts ...grpc.CallOption) (*GetPredecessorAndSuccessorsResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(GetPredecessorAndSuccessorsResponse)
	err := c.cc.Invoke(ctx, Chord_GetPredecessorAndSuccessors_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *chordClient) FindSuccessor(ctx context.Context, in *FindSuccessorRequest, opts ...grpc.CallOption) (*FindSuccessorResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(FindSuccessorResponse)
	err := c.cc.Invoke(ctx, Chord_FindSuccessor_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// ChordServer is the server API for Chord service.
// All implementations must embed UnimplementedChordServer
// for forward compatibility.
type ChordServer interface {
	Ping(context.Context, *PingRequest) (*PingResponse, error)
	Put(context.Context, *PutRequest) (*PutResponse, error)
	Get(context.Context, *GetRequest) (*GetResponse, error)
	Delete(context.Context, *DeleteRequest) (*DeleteResponse, error)
	GetAll(context.Context, *GetAllRequest) (*GetAllResponse, error)
	PutAll(context.Context, *PutAllRequest) (*PutAllResponse, error)
	GetSome(context.Context, *GetSomeRequest) (*GetSomeResponse, error)
	Notify(context.Context, *NotifyRequest) (*NotifyResponse, error)
	GetPredecessorAndSuccessors(context.Context, *GetPredecessorAndSuccessorsRequest) (*GetPredecessorAndSuccessorsResponse, error)
	FindSuccessor(context.Context, *FindSuccessorRequest) (*FindSuccessorResponse, error)
	mustEmbedUnimplementedChordServer()
}

// UnimplementedChordServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedChordServer struct{}

func (UnimplementedChordServer) Ping(context.Context, *PingRequest) (*PingResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Ping not implemented")
}
func (UnimplementedChordServer) Put(context.Context, *PutRequest) (*PutResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Put not implemented")
}
func (UnimplementedChordServer) Get(context.Context, *GetRequest) (*GetResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Get not implemented")
}
func (UnimplementedChordServer) Delete(context.Context, *DeleteRequest) (*DeleteResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Delete not implemented")
}
func (UnimplementedChordServer) GetAll(context.Context, *GetAllRequest) (*GetAllResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetAll not implemented")
}
func (UnimplementedChordServer) PutAll(context.Context, *PutAllRequest) (*PutAllResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method PutAll not implemented")
}
func (UnimplementedChordServer) GetSome(context.Context, *GetSomeRequest) (*GetSomeResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetSome not implemented")
}
func (UnimplementedChordServer) Notify(context.Context, *NotifyRequest) (*NotifyResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Notify not implemented")
}
func (UnimplementedChordServer) GetPredecessorAndSuccessors(context.Context, *GetPredecessorAndSuccessorsRequest) (*GetPredecessorAndSuccessorsResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetPredecessorAndSuccessors not implemented")
}
func (UnimplementedChordServer) FindSuccessor(context.Context, *FindSuccessorRequest) (*FindSuccessorResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method FindSuccessor not implemented")
}
func (UnimplementedChordServer) mustEmbedUnimplementedChordServer() {}
func (UnimplementedChordServer) testEmbeddedByValue()               {}

// UnsafeChordServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to ChordServer will
// result in compilation errors.
type UnsafeChordServer interface {
	mustEmbedUnimplementedChordServer()
}

func RegisterChordServer(s grpc.ServiceRegistrar, srv ChordServer) {
	// If the following call pancis, it indicates UnimplementedChordServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&Chord_ServiceDesc, srv)
}

func _Chord_Ping_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PingRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).Ping(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_Ping_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).Ping(ctx, req.(*PingRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_Put_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PutRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).Put(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_Put_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).Put(ctx, req.(*PutRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_Get_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).Get(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_Get_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).Get(ctx, req.(*GetRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_Delete_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DeleteRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).Delete(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_Delete_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).Delete(ctx, req.(*DeleteRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_GetAll_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetAllRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).GetAll(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_GetAll_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).GetAll(ctx, req.(*GetAllRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_PutAll_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PutAllRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).PutAll(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_PutAll_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).PutAll(ctx, req.(*PutAllRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_GetSome_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetSomeRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).GetSome(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_GetSome_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).GetSome(ctx, req.(*GetSomeRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_Notify_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(NotifyRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).Notify(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_Notify_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).Notify(ctx, req.(*NotifyRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_GetPredecessorAndSuccessors_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetPredecessorAndSuccessorsRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).GetPredecessorAndSuccessors(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_GetPredecessorAndSuccessors_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).GetPredecessorAndSuccessors(ctx, req.(*GetPredecessorAndSuccessorsRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Chord_FindSuccessor_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FindSuccessorRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ChordServer).FindSuccessor(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Chord_FindSuccessor_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ChordServer).FindSuccessor(ctx, req.(*FindSuccessorRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Chord_ServiceDesc is the grpc.ServiceDesc for Chord service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Chord_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "chord.Chord",
	HandlerType: (*ChordServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Ping",
			Handler:    _Chord_Ping_Handler,
		},
		{
			MethodName: "Put",
			Handler:    _Chord_Put_Handler,
		},
		{
			MethodName: "Get",
			Handler:    _Chord_Get_Handler,
		},
		{
			MethodName: "Delete",
			Handler:    _Chord_Delete_Handler,
		},
		{
			MethodName: "GetAll",
			Handler:    _Chord_GetAll_Handler,
		},
		{
			MethodName: "PutAll",
			Handler:    _Chord_PutAll_Handler,
		},
		{
			MethodName: "GetSome",
			Handler:    _Chord_GetSome_Handler,
		},
		{
			MethodName: "Notify",
			Handler:    _Chord_Notify_Handler,
		},
		{
			MethodName: "GetPredecessorAndSuccessors",
			Handler:    _Chord_GetPredecessorAndSuccessors_Handler,
		},
		{
			MethodName: "FindSuccessor",
			Handler:    _Chord_FindSuccessor_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "chord.proto",
}
